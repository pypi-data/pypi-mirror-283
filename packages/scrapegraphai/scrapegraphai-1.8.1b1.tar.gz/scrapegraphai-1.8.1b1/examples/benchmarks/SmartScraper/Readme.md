# Local models
The two websites benchmark are:
- Example 1:  https://perinim.github.io/projects
- Example 2: https://www.wired.com (at 17/4/2024)

Both are strored locally as txt file in .txt format  because in this way we do not have to think about the internet connection

| Hardware           | Model                                   | Example 1 | Example 2 |
| ------------------ | --------------------------------------- | --------- | --------- |
| Macbook 14' m1 pro | Mistral on Ollama with nomic-embed-text | 11.60s    | 26.61s    |
| Macbook m2 max     | Mistral on Ollama with nomic-embed-text | 8.05s     | 12.17s    |
| Macbook 14' m1 pro | Llama3 on Ollama with nomic-embed-text  | 29.87s    | 35.32s    |
| Macbook m2 max     | Llama3 on Ollama with nomic-embed-text  | 18.36s    | 78.32s    |

**Note**: the examples on Docker are not runned on other devices than the Macbook because the performance are to slow (10 times slower than Ollama). Indeed the results are the following:

| Hardware           | Example 1 | Example 2 |
| ------------------ | --------- | --------- |
| Macbook 14' m1 pro | 139.89    | Too long  |
# Performance on APIs services
### Example 1: personal portfolio 
**URL**: https://perinim.github.io/projects
**Task**: List me all the projects with their description.

| Name                        | Execution time (seconds) | total_tokens | prompt_tokens | completion_tokens | successful_requests | total_cost_USD |
| --------------------------- | ------------------------ | ------------ | ------------- | ----------------- | ------------------- | -------------- |
| gpt-3.5-turbo               | 25.22                    | 445          | 272           | 173               | 1                   | 0.000754       |
| gpt-4-turbo-preview         | 9.53                     | 449          | 272           | 177               | 1                   | 0.00803        |
| Grooq with nomic-embed-text | 1.99                     | 474          | 284           | 190               | 1                   | 0              |

### Example 2: Wired
**URL**: https://www.wired.com
**Task**: List me all the articles with their description.

| Name                        | Execution time (seconds) | total_tokens | prompt_tokens | completion_tokens | successful_requests | total_cost_USD |
| --------------------------- | ------------------------ | ------------ | ------------- | ----------------- | ------------------- | -------------- |
| gpt-3.5-turbo               | 25.89                    | 445          | 272           | 173               | 1                   | 0.000754       |
| gpt-4-turbo-preview         | 64.70                    | 3573         | 2199          | 1374              | 1                   | 0.06321        |
| Grooq with nomic-embed-text | 3.82                     | 2459         | 2192          | 267               | 1                   | 0              |


