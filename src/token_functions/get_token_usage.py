"""
Last Updated: May 22, 2025
Author: Max Freitas
File Purpose: Calculate token usage of ChatGPT models to get understanding of cost
"""


def get_token_usage(response, input_cost_per_million: float, output_cost_per_million: float) -> dict:
    def calculate_cost(tokens: int, rate_per_million: float) -> float:
        return (tokens * rate_per_million) / 1000000

    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    prompt_cost = round(calculate_cost(prompt_tokens, input_cost_per_million), 2)
    completion_cost = round(calculate_cost(completion_tokens, output_cost_per_million),2)
    total_cost = round(prompt_cost + completion_cost, 2)
    estimated_cost_per_12k_images = round(total_cost * 12000, 2)

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "prompt_tokens_cost": prompt_cost,
        "completion_tokens_cost": completion_cost,
        "total_cost": total_cost,
        "estimated_cost_per_12000_images": estimated_cost_per_12k_images
    }