import json
import re
import math

def greeting_protocol(user_message):
    """Determine the appropriate greeting based on user message content."""
    # Check for urgency keywords
    urgency_keywords = ["urgent", "asap", "emergency"]
    if any(keyword in user_message.lower() for keyword in urgency_keywords):
        return "CloudResource-JSON-AI here! Let's quickly optimize your server resources."
    
    # Check for name in the message
    name_match = re.search(r"(?i)my name is (\w+)|I am (\w+)|I'm (\w+)", user_message)
    if name_match:
        name = next(group for group in name_match.groups() if group is not None)
        return f"Hello, {name}! I'm CloudResource-JSON-AI, here to assist with your resource allocation."
    
    # Check for tone indicators
    happy_keywords = ["happy", "excited", "joyful", "great"]
    sad_keywords = ["sad", "down", "unhappy"]
    angry_keywords = ["angry", "mad", "frustrated"]
    
    if any(keyword in user_message.lower() for keyword in happy_keywords):
        return "Hello! It's great to see your positive energy. I'm here to help optimize your server resources!"
    if any(keyword in user_message.lower() for keyword in sad_keywords):
        return "Hello. I'm sorry you're feeling down. I'm here to help optimize your server resources."
    if any(keyword in user_message.lower() for keyword in angry_keywords):
        return "Hello. I understand you're frustrated. Let's work together to optimize your server resources."
    
    # Default greeting
    return "Greetings! I am CloudResource-JSON-AI, your cloud resource optimization assistant. Please provide your server resource data in JSON format to begin."

def provide_template():
    """Return the JSON template for data input."""
    return """Here is the template:

JSON Format Example:
```json
{
 "resources": [
 {
 "resource_id": "[String]",
 "current_load": [Integer],
 "max_capacity": [Integer],
 "real_time_usage": [Integer]
 }
 ]
}
```

Please provide your server resource data in JSON format to begin the optimization analysis."""

def validate_json_data(json_data):
    """Validate JSON data structure and fields."""
    errors = []
    
    # Check if resources key exists
    if "resources" not in json_data:
        errors.append("ERROR: Missing 'resources' array in the JSON input.")
        return errors, None
    
    resources = json_data["resources"]
    
    if not isinstance(resources, list):
        errors.append("ERROR: 'resources' must be an array.")
        return errors, None
    
    if len(resources) == 0:
        errors.append("ERROR: 'resources' array cannot be empty.")
        return errors, None
    
    # Validate each resource record
    required_fields = ["resource_id", "current_load", "max_capacity", "real_time_usage"]
    numeric_fields = ["current_load", "max_capacity", "real_time_usage"]
    
    for i, resource in enumerate(resources):
        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in resource]
        if missing_fields:
            errors.append(f"ERROR: Missing required field(s): {', '.join(missing_fields)} in record {i+1}.")
        
        # Check data types for numeric fields
        invalid_type_fields = []
        for field in numeric_fields:
            if field in resource and not isinstance(resource[field], (int, float)):
                invalid_type_fields.append(field)
        
        if invalid_type_fields:
            errors.append(f"ERROR: Invalid data type for the field(s): {', '.join(invalid_type_fields)} in record {i+1}. Please ensure numeric values.")
        
        # Check value ranges for numeric fields
        invalid_value_fields = []
        for field in numeric_fields:
            if field in resource and isinstance(resource[field], (int, float)):
                if resource[field] <= 0 or resource[field] > 100:
                    invalid_value_fields.append(field)
        
        if invalid_value_fields:
            errors.append(f"ERROR: Invalid value for the field(s): {', '.join(invalid_value_fields)} in record {i+1}. Please make sure that all data falls within the range of 1 to 100.")
    
    # Return validation results
    if errors:
        return errors, None
    
    return [], resources

def calculate_resource_metrics(resource):
    """Calculate metrics for a single resource."""
    # Extract the input data
    resource_id = resource["resource_id"]
    current_load = resource["current_load"]
    max_capacity = resource["max_capacity"]
    real_time_usage = resource["real_time_usage"]
    
    # Calculate available capacity
    available_capacity = round(max_capacity - current_load, 2)
    
    # Calculate utilization ratio
    utilization_ratio = round((current_load / max_capacity) * 100, 2)
    
    # Check scaling requirements
    demand_increasing = real_time_usage > current_load
    scaling_required = available_capacity < 20
    
    # Calculate additional capacity needed if scaling is required
    additional_capacity_needed = None
    if scaling_required:
        additional_capacity_needed = round(100 - current_load, 2)
    
    return {
        "resource_id": resource_id,
        "current_load": current_load,
        "max_capacity": max_capacity,
        "real_time_usage": real_time_usage,
        "available_capacity": available_capacity,
        "utilization_ratio": utilization_ratio,
        "demand_increasing": demand_increasing,
        "scaling_required": scaling_required,
        "additional_capacity_needed": additional_capacity_needed
    }

def generate_validation_report(resources):
    """Generate data validation report section."""
    num_resources = len(resources)
    first_resource = resources[0]
    num_fields = len(first_resource)
    
    report = f"""# Data Validation Report
## 1. Data Structure Check:
- Number of resources: {num_resources}
- Number of fields per record: {num_fields}

## 2. Required Fields Check:
- resource_id: present
- current_load: present
- max_capacity: present
- real_time_usage: present

## 3. Data Type and Value Validation:
- current_load (positive number, ≤ 100): validated
- max_capacity (positive number, ≤ 100): validated
- real_time_usage (positive number, ≤ 100): validated

## Validation Summary:
Data validation is successful! Proceeding with analysis...
"""
    return report

def generate_calculation_formulas():
    """Generate the calculation formulas section."""
    return """# Calculation Formulas:
1. Available Capacity:
$$
\\text{Available Capacity} = \\text{max_capacity} - \\text{current_load}
$$
2. Additional Capacity Needed (if scaling required):
$$
\\text{Additional Capacity Needed} = 100 - \\text{current_load}
$$
"""

def generate_resource_analysis(metrics):
    """Generate detailed analysis for a single resource."""
    resource_id = metrics["resource_id"]
    current_load = metrics["current_load"]
    max_capacity = metrics["max_capacity"]
    real_time_usage = metrics["real_time_usage"]
    available_capacity = metrics["available_capacity"]
    utilization_ratio = metrics["utilization_ratio"]
    demand_increasing = metrics["demand_increasing"]
    scaling_required = metrics["scaling_required"]
    additional_capacity_needed = metrics["additional_capacity_needed"]
    
    # Prepare scaling requirement check responses
    if demand_increasing:
        demand_explanation = f"All the detailed explanation here: The real-time usage {real_time_usage} exceeds the current load {current_load}, indicating that the demand on the resource is increasing."
    else:
        demand_explanation = f"All the detailed explanation here: The real-time usage {real_time_usage} does not exceed the current load {current_load}, indicating that the demand on the resource is stable."
    
    if available_capacity < 20:
        capacity_explanation = "Since the available capacity is below the explicit threshold of 20%, scaling up is required to handle increased demand."
    else:
        capacity_explanation = "Available capacity is above the threshold of 20%, indicating sufficient resource allocation."
    
    # Determine final scaling recommendation
    if demand_increasing and scaling_required:
        scaling_response = "Real-time usage exceeds current load, and available capacity is below 20%. Scaling up is required."
        final_recommendation = f"Scaling up is recommended for {resource_id} to achieve optimal load balance."
    elif demand_increasing or scaling_required:
        if demand_increasing:
            scaling_response = "Real-time usage exceeds current load, indicating increased demand. Scaling up may be needed."
        else:
            scaling_response = "Available capacity is below 20%. Scaling up is required to handle demand."
        final_recommendation = f"Scaling up is recommended for {resource_id} to achieve optimal load balance."
    else:
        scaling_response = "Resource allocation is currently sufficient."
        final_recommendation = f"No scaling is required for {resource_id}; resource allocation is optimal."
    
    # Prepare allocation adjustment response
    if scaling_required:
        allocation_response = f"The additional capacity needed is {additional_capacity_needed}%."
        allocation_calculation = f"""$$
100 - {current_load} = {additional_capacity_needed}
$$"""
    else:
        allocation_response = "Current resource allocation is optimal; no additional capacity is needed."
        allocation_calculation = "Not applicable as scaling is not required."
    
    analysis = f"""## Resource {resource_id}
### Input Data:
- Current Load: {current_load}%
- Maximum Capacity: {max_capacity}%
- Real-time Usage: {real_time_usage}%

### Detailed Calculations:
1. **Available Capacity Calculation:**
 - Formula:
 $$
 \\text{{Available Capacity}} = \\text{{max_capacity}} - \\text{{current_load}}
 $$
 - Calculation:
 $$
     {max_capacity} - {current_load} = {available_capacity}\\ \\%
 $$
 - Explanation: This step subtracts the current load from the maximum capacity to determine how much capacity is still available.
 - System Response: "The available capacity is {available_capacity}%."

2. **Resource Utilization Ratio**
- Formula:
 $$ \\text{{Utilization Ratio (\\%)}} = \\left(\\frac{{\\text{{current_load}}}}{{\\text{{max_capacity}}}}\\right) \\times 100 $$
- Calculation:
 $$ \\left(\\frac{{{current_load}}}{{{max_capacity}}}\\right) \\times 100 = {utilization_ratio}\\% $$
- Explanation:
 This metric provides a direct percentage of how much capacity is being used. A high utilization ratio (close to 100%) may signal that resources are nearly maxed out and could benefit from scaling.
 - System Response: "The Utilization Ratio is {utilization_ratio}%."

3. **Scaling Requirement Check:**
 - Condition 1:  
 IF real_time_usage > current_load, THEN scaling up is required.  
 Detailed Explanation: "{demand_explanation}"
 - Condition 2:  
 IF available_capacity < 20, THEN scaling up is required.  
 Detailed Explanation: "{capacity_explanation}"
 - System Response:  
 {scaling_response}

4. **Optimal Allocation Adjustment:**
 - If scaling up is required, THEN calculate:
 $$
 \\text{{Additional Capacity Needed}} = 100 - \\text{{current_load}}
 $$
 - Calculation:
 {allocation_calculation}
 - Explanation: This calculation determines the additional capacity needed to reach full utilization (100%). It shows step-by-step how the additional capacity is derived.
 - System Response: "{allocation_response}"

### Final Recommendation:
{final_recommendation}
"""
    return analysis

def generate_full_report(resources):
    """Generate the full analysis report."""
    # Calculate metrics for each resource
    all_metrics = [calculate_resource_metrics(resource) for resource in resources]
    
    # Generate report sections
    validation_report = generate_validation_report(resources)
    calculation_formulas = generate_calculation_formulas()
    
    # Generate resource allocation analysis section
    resource_analysis_header = f"""# Resource Allocation Analysis
Total Resources Evaluated: {len(resources)}

# Detailed Analysis
"""
    
    # Generate detailed analysis for each resource
    detailed_analyses = "\n".join([generate_resource_analysis(metrics) for metrics in all_metrics])
    
    # Combine all sections
    full_report = f"""{validation_report}

{calculation_formulas}

{resource_analysis_header}
{detailed_analyses}

# Feedback and Rating Request
Would you like detailed calculations for any specific resource? Please rate this analysis on a scale of 1-5.
"""
    
    return full_report

def process_feedback(rating):
    """Process user feedback based on rating."""
    if rating == 1:
        return "We are very sorry that the analysis did not meet your expectations. Could you please provide specific feedback on what went wrong?"
    elif rating == 2:
        return "Thank you for your feedback. We appreciate your input and would love to know more details on how we can improve."
    elif rating == 3:
        return "Thank you for your feedback. We are committed to continuous improvement. Could you share what aspects need enhancement?"
    elif rating == 4:
        return "Thank you for your positive feedback! We're glad the analysis was helpful."
    elif rating == 5:
        return "Thank you for your excellent feedback! We are thrilled to have met your expectations and appreciate your input."
    else:
        return "Thank you for your feedback. Please rate on a scale of 1-5 for a more specific response."

def main():
    """Main function to execute the CloudResource-JSON-AI workflow with sample data."""
    # Sample JSON data - includes scenarios with different scaling requirements
    sample_json_data = {
  "resources": [
    {
      "resource_id": "server1",
      "current_load": 65,
      "max_capacity": 80,
      "real_time_usage": 70
    },
    {
      "resource_id": "server2",
      "current_load": 50,
      "max_capacity": 70,
      "real_time_usage": 55
    },
    {
      "resource_id": "server3",
      "current_load": 75,
      "max_capacity": 90,
      "real_time_usage": 80
    },
    {
      "resource_id": "server4",
      "current_load": 45,
      "max_capacity": 65,
      "real_time_usage": 50
    },
    {
      "resource_id": "server5",
      "current_load": 80,
      "max_capacity": 95,
      "real_time_usage": 85
    },
    {
      "resource_id": "server6",
      "current_load": 60,
      "max_capacity": 80,
      "real_time_usage": 65
    },
    {
      "resource_id": "server7",
      "current_load": 55,
      "max_capacity": 75,
      "real_time_usage": 60
    },
    {
      "resource_id": "server8",
      "current_load": 40,
      "max_capacity": 60,
      "real_time_usage": 45
    }
  ]
}

    
    print("CloudResource-JSON-AI Analysis")
    print("===============================")
    print()
    print("Processing sample JSON data:")
    print(json.dumps(sample_json_data, indent=2))
    print()
    
    # Validate JSON structure and fields
    errors, resources = validate_json_data(sample_json_data)
    if errors:
        for error in errors:
            print(error)
        return
    
    # Generate and print the full report
    full_report = generate_full_report(resources)
    print(full_report)

if __name__ == "__main__":
    main()