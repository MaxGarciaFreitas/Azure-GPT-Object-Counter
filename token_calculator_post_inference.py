"""
Last Updated: May 22, 2025
Author: Max Freitas
File Purpose: To calculate expected cost of models in tokens based on known input and expected output
"""
import tiktoken

def token_calculator_post(input_num_tokens, output_num_tokens, input_cost_per_million= 2, output_cost_per_million= 8, num_images=1):

  # input tokens
  input_tokens_cost = input_num_tokens * input_cost_per_million / 1000000
  print(f'Cost of Input tokens per {num_images} images: {input_tokens_cost* num_images}')

  # output tokens
  output_tokens_cost = output_num_tokens * output_cost_per_million / 1000000
  print(f'Cost of Expected tokens per {num_images} images: {output_tokens_cost* num_images}')

  # total cost
  total_cost = round((input_tokens_cost + output_tokens_cost)*num_images,4)
  print(f"Total cost per {num_images} images: {total_cost}")


def token_calculator_based_on_prompt(prompt_text, sample_output, model= "gpt-4", input_cost_per_million= 2, output_cost_per_million= 8, num_images=10000):
  enc = tiktoken.encoding_for_model(model)

  # calculate input tokens
  input_tokens = enc.encode(prompt_text)
  input_num_tokens = len(input_tokens)
  print(f"Number of input tokens: {input_num_tokens}")
  input_tokens_cost = input_num_tokens * input_cost_per_million / 1000000
  print(f'Cost of Input tokens per {num_images} images: {input_tokens_cost* num_images}')

  # calculate expected output tokens
  output_tokens = enc.encode(sample_output)
  expected_num_tokens = len(output_tokens)
  print(f"\nExpected number of output tokens: {expected_num_tokens}")
  expected_tokens_cost = expected_num_tokens * output_cost_per_million / 1000000
  print(f'Cost of Expected tokens per {num_images} images: {expected_tokens_cost* num_images}')

  # total cost
  total_cost = round((input_tokens_cost + expected_tokens_cost)*num_images,4)
  print(f"Total cost per {num_images} images: {total_cost}")