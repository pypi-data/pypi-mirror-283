"""
Contains methods for calculating various spectra from a structure, and converting between
different types of spectra.
"""

import torch
from gbsd import structure


def get_distance_matrix(
    points_1: torch.Tensor,
    points_2: torch.Tensor,
    supercell_vectors: torch.Tensor
) -> torch.Tensor:
    """Gets distance matrix while accounting for minimal image convention.

    Args:
    - `points_1`: Tensor with shape M x D.
    - `points_2`: Tensor with shape N x D.
    - `supercell_vectors`: D x D tensor of supercell vectors, e.g., [[ a1 ], [ a2 ], [ a3 ]].

    Returns: M x N tensor of distances.
    """
    pair_differences = points_2[None, :, :] - points_1[:, None, :]

    pair_differences_shifts = torch.round(pair_differences @ supercell_vectors.inverse()) @ supercell_vectors
    image_pair_differences = pair_differences - pair_differences_shifts

    distance_matrix = torch.linalg.norm(image_pair_differences, dim=-1)

    return distance_matrix


def get_observed_distances(
    points_1: torch.Tensor,
    points_2: torch.Tensor,
    supercell_vectors: torch.Tensor
) -> torch.Tensor:
    """Gets the list of observed distances between two sets of points in D dimensions.
    
    If the points are identical, symmetry and zeros are ignored.

    Args:
    - `points_1`: Tensor with shape M x D
    - `points_2`: Tensor with shape N x D
    - `supercell_vectors`: D x D tensor of supercell vectors, e.g., [[ a1 ], [ a2 ], [ a3 ]].
    
    Returns: 1D tensor of observed distances.
    """
    distance_matrix = get_distance_matrix(points_1, points_2, supercell_vectors)

    if points_1 is points_2:
        # Ignore zeros if identical tensors given
        off_diagonal_mask = (1 - torch.eye(*distance_matrix.shape, device=distance_matrix.device)).bool()
        observed_distances = distance_matrix[off_diagonal_mask]
    else:
        observed_distances = torch.flatten(distance_matrix)

    return observed_distances


def get_partial_rdf(
    points_1: torch.Tensor,
    points_2: torch.Tensor,
    supercell_vectors: torch.Tensor,
    bins: torch.Tensor,
    kernel_width: float = 0.05,
) -> torch.Tensor:
    """Gets the partial radial distribution function (RDF) between two sets of points.

    Note: Uses kernel density estimation (KDE) with Gaussians so that the output is differentiable.

    Args:
    - `points_1`: Tensor with shape M x D.
    - `points_2`: Tensor with shape N x D.
    - `supercell_vectors`: D x D tensor of supercell vectors, e.g., [[ a1 ], [ a2 ], [ a3 ]].
    - `bins`: The values of $r$ on which to evaluate the partial RDF.
    - `kernel_width`: Width of Gaussians for KDE. You should use a value less than half the width
    of the smallest expected peak. Using a good value may require trial and error.
    
    Returns: 1D tensor of estimated partial RDF values evaluated on `bins`.
    """
    observed_distances = get_observed_distances(points_1, points_2, supercell_vectors)

    gaussians: torch.Tensor = torch.exp(
        -0.5 * ((bins - observed_distances.view(-1, 1)) / kernel_width)**2
    ) / (kernel_width * (2 * torch.pi)**0.5)

    summed_gaussians = gaussians.sum(dim=0)

    volume = structure.get_cell_volume(supercell_vectors)
    partial_rdf = (volume / (observed_distances).size(0)) * (1 / (4 * torch.pi * bins**2)) * summed_gaussians

    return partial_rdf

def get_neutron_total_rdf(
    species_positions: dict[str, torch.Tensor] | torch.nn.ParameterDict,
    supercell_vectors: torch.Tensor,
    bins: torch.Tensor,
    scattering_lengths: dict[str, float],
    kernel_width: float = 0.05,
) -> torch.Tensor:
    """Calculates the total radial distribution function (RDF), G(r), for a structure.
    
    G(r) is defined as in "Keen. J. Appl. Crystallogr. (2001). 34, 172-177."

    Outputs in units of barns when scattering_lengths are in femtometers.

    Note: Uses kernel density estimation (KDE) with Gaussians so that the output is differentiable.

    Args:
    - `species_positions`: Dictionary that maps element labels to Tensor of positions. If you are
    optimizing the positions in a Model, you should use a torch.nn.ParameterDict.
    - `supercell_vectors`: D x D tensor of supercell vectors, e.g., [[ a1 ], [ a2 ], [ a3 ]].
    - `bins`: The values of $r$ on which to evaluate the total RDF.
    - `scattering_lengths`: Dictionary that maps element labels to the element's average coherent
    bound neutron scattering length. Use units of femtometers.
    - `kernel_width`: Width of Gaussians for KDE. You should use a value less than half the width
    of the smallest expected peak in each partial RDF. Using a good value may require trial and
    error.

    Returns: 1D tensor of estimated total RDF values evaluated on `bins`.
    """
    # volume = structure.get_cell_volume(supercell_vectors)
    total_particle_count = sum(positions.size(0) for positions in species_positions.values())
    # total_density = total_particle_count / volume

    species_fraction = {
        species: positions.size(0) / total_particle_count for species, positions in species_positions.items()
    }

    total_rdf = torch.zeros_like(bins)
    for species_1, positions_1 in species_positions.items():
        for species_2, positions_2 in species_positions.items():
            fraction_1 = species_fraction[species_1]
            fraction_2 = species_fraction[species_2]
            scattering_length_1 = scattering_lengths[species_1]
            scattering_length_2 = scattering_lengths[species_2] 

            coefficient = fraction_1 * fraction_2 * scattering_length_1 * scattering_length_2 * 0.01

            partial_rdf = get_partial_rdf(
                positions_1,
                positions_2,
                supercell_vectors,
                bins,
                kernel_width
            )

            total_rdf += coefficient * (partial_rdf - 1)

    return total_rdf


def get_total_correlation_function(
    total_rdf: torch.Tensor,
    r_bins: torch.Tensor,
    scattering_lengths: dict[str, float] | dict[str, torch.Tensor],
    total_density: float | torch.Tensor,
    species_fractions: dict[str, float] | dict[str, torch.Tensor], 
):
    """Calculates the total correlation function, T(r), from the total RDF.

    T(r) is defined as in "Keen. J. Appl. Crystallogr. (2001). 34, 172-177."

    You can get the `total_rdf` from `get_neutron_total_rdf(...)`.

    Args:
    - `total_rdf`: 1D tensor of total radial distribution function values evaluated on `r_bins`.
    - `r_bins`: The values of $r$ on which the total_rdf is evaluated.
    - `scattering_lengths`: Dictionary that maps element labels to the element's average coherent
    bound neutron scattering length. Use units of femtometers.
    - `total_density`: The total number density of the system.
    - `species_fractions`: Dictionary that maps element labels to the element's mole fraction in
    the structure.

    Returns: 1D tensor of the total correlation function, T(r), evaluated on r_bins.
    """
    rdf_offset = (sum(fraction * scattering_lengths[species] for species, fraction in species_fractions.items()))**2

    return 4 * torch.pi * r_bins * total_density * (total_rdf + rdf_offset)
    


def get_neutron_total_scattering_sf(
    total_rdf: torch.Tensor,
    r_bins: torch.Tensor,
    q_bins: torch.Tensor,
    total_density: torch.Tensor | float,
) -> torch.Tensor:
    """Calculates the total scattering structure factor (SF), F(Q) = i(Q), from the total RDF.

    F(Q) = i(Q) is defined as in "Keen. J. Appl. Crystallogr. (2001). 34, 172-177."

    You can get the `total_rdf` from `get_neutron_total_rdf(...)`.

    Note: It is important for the accuracy of this calculation that `r_bins` is large enough that
    the `total_rdf` becomes close to zero.

    Args:
    - `total_rdf`: 1D tensor of total radial distribution function values evaluated on `r_bins`.
    - `r_bins`: The values of $r$ on which the total_rdf is evaluated.
    - `q_bins`: The values of $Q$ on which to evaluate the total scattering SF.
    - `total_density`: The total number density of the system.

    Returns: 1D tensor of estimated total-scattering SF values, evaluated on q_bins.
    """
    integrand = r_bins[None, :] * total_rdf[None, :] * torch.sin(q_bins[:, None] * r_bins[None, :]) / q_bins[:, None]

    total_scattering_sf = 4 * torch.pi * total_density * torch.trapz(integrand, r_bins)
    return total_scattering_sf
