# Bicycle Inventory Application
## Running the Application with Docker
### Step 1: Build the Docker Image

```docker build -t bicycle_inventory_app:latest .```

### Step 2: Run the Application

### Use the following command to run the application inside a Docker container:

```docker run --rm bicycle_inventory_app:latest <function1> [function2 ...]```

### Available Functions:
```
filter
brand_count
sort
gbp_per_kg
Examples: 
```
### Run the filter function:

```docker run --rm bicycle_inventory_app:latest filter```
### Run multiple functions in sequence:

```docker run --rm bicycle_inventory_app:latest filter sort```

### Output result to another file:

```docker run --rm bicycle_inventory_app:latest filter > filtered_invetory.json```
### The application automatically cleans the data before executing the specified functions.

## Short Usage Guide
filter: Filters in-stock mountain bikes priced at £1000 or more.
brand_count: Counts the number of bicycles per brand.
sort: Sorts bicycles by price and weight.
gbp_per_kg: Calculates the price per kilogram for each bicycle.
Note: Replace <function1> [function2 ...] with one or more functions from the list above to perform the desired operations.
