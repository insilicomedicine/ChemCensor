from enum import IntEnum


class CompositionConfig(IntEnum):
    """Configuration for database composition.

    Specifies two parameters: batch_size and distributivity
    threshold. The latter one determines how many reaction examples
    the multi-component center should have for applying
    distributivity of its FG bits based on bits from individual
    components
    """

    default_batch_size = 32
    distributivity_threshold = 2
