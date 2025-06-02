# **Secure Computing using Azure API for ChatGPT-based Object Counting in Images**  
![Azure AI Vision](https://azure.microsoft.com/svghandler/ai-vision/?width=600&height=300)  

---  
## **Project Overview**  
Leverage **ChatGPT-4o via Azure API** to count objects in images while maintaining:  
🔒 **HIPAA/GDPR Compliance**  
💰 **Cost-Efficient Processing**  
⚡ **Low-Latency Inference**  

---  
## **Prerequisites**  
Before you begin:  
- [x] Azure subscription with OpenAI access  
- [x] Python 3.8+ installed  
- [x] Azure CLI configured (`az login`)  

---  
## **Setup Instructions**  

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Demo: Configure API Credentials**  
Edit `/src/demo/api_test.py`:  

```python
# Azure OpenAI Configuration
endpoint = os.getenv("ENDPOINT_URL", "https://your-resource.openai.azure.com")  # Replace with your endpoint
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")  # Your deployed model name
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "your-api-key-here")  # Keep this secure!
api_version = "2023-05-15"  # Check Azure portal for latest
```

Check: if output prints successfuly in terminal, if so continue to step 3

### 3. **Run Inference**
Edit `inference.py`

```python
# Azure OpenAI Configuration
endpoint = os.getenv("ENDPOINT_URL", "https://your-resource.openai.azure.com")  # Replace with your endpoint
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")  # Your deployed model name
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "your-api-key-here")  # Keep this secure!
api_version = "2023-05-15"  # Check Azure portal for latest
```
If output (`src\demo\test_animal_output.json`) matches below, everything is working as intended
```bash
{
    "image_name": "test_animals.jpeg",
    "output_json_name": "test_animals_output.json",
    "output_dir": "DIRECTORY",
    "image_metadata": {
        "original_image_size": [
            560,
            373
        ],
        "resized_and_padded_size": [
            640,
            640
        ]
    },
    "detections": {
        "Snakes": 1,
        "Turtles": 2
    },
    "model_metadata": {
        "model_version": "gpt-4o",
        "timestamp": "2025-06-02T16:36:08.297794Z",
        "input_message": "Count the number of snakes, and turtles in the image. Return the result in this exact format: {Snakes: <number>, Turtles: <number>}. If none are present, return 0 for each."
    },
    "python_metadata": {},
    "token_usage": {
        "prompt_tokens": 817,
        "completion_tokens": 13,
        "total_tokens": 830,
        "prompt_tokens_cost": 0.001634,
        "completion_tokens_cost": 0.000104,
        "total_cost": 0.001738,
        "total_cost_per_12000_images": 20.856
    }
}
```

### 4, **Future Steps**
- Experiment with different prompts
- Try different deployments
  
