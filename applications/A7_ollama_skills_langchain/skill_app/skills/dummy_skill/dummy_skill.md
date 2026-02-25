---
name: dummy-skill
description: Helps with basic mathematical calculations and unit conversions. Use when users ask for arithmetic operations, unit conversions (length, weight, temperature), or percentage calculations.
---

When helping with calculations and conversions, always include:

## Instructions

### Mathematical Operations
1. **Show your work**: Perform calculations step by step
2. **Be clear**: Display each step of the calculation
3. **Verify**: Double-check the result before presenting it
4. **Round appropriately**: Use 2 decimal places unless specified otherwise

### Unit Conversions
Common conversions to support:

**Length:**
- 1 meter = 3.28084 feet
- 1 kilometer = 0.621371 miles
- 1 inch = 2.54 centimeters

**Weight:**
- 1 kilogram = 2.20462 pounds
- 1 pound = 0.453592 kilograms
- 1 ounce = 28.3495 grams

**Temperature:**
- Celsius to Fahrenheit: (C × 9/5) + 32
- Fahrenheit to Celsius: (F - 32) × 5/9

### Percentage Calculations
- To find X% of Y: (X/100) × Y
- To find what percentage X is of Y: (X/Y) × 100
- To increase Y by X%: Y × (1 + X/100)
- To decrease Y by X%: Y × (1 - X/100)

## Response Format
Structure your answer as:
1. **Problem statement**: Restate what needs to be calculated
2. **Formula or method**: Show the formula being used
3. **Calculation steps**: Work through the math step by step
4. **Final answer**: Present the result with appropriate units

## Example Usage

**User:** "What is 15% of 240?"

**Response:**
- Problem: Find 15% of 240
- Formula: (15/100) × 240
- Calculation: 0.15 × 240 = 36
- Answer: 15% of 240 is 36

**User:** "Convert 10 miles to kilometers"

**Response:**
- Problem: Convert 10 miles to kilometers
- Conversion: 1 mile = 1.60934 kilometers
- Calculation: 10 × 1.60934 = 16.0934
- Answer: 10 miles equals approximately 16.09 kilometers

Keep explanations clear and conversational. For complex calculations, break them down into smaller, manageable steps.
