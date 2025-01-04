# Data Processing

## Table of Contents

- [Data Processing](#data-processing)
  - [Table of Contents](#table-of-contents)
  - [Preprocessing](#preprocessing)
  - [Feature Selection](#feature-selection)
  - [Scaling](#scaling)
  - [Dimensionality Reduction](#dimensionality-reduction)
  - [References](#references)

## Preprocessing

Identifying and zero variance features were removed.

<details>

<summary> The removed features (click to expand) </summary>

- Identifying features
  - src
  - dst
  - table_id
  - in_port
  - dl_dst
- Zero variance features
  - port_rx_dropped
  - port_tx_dropped
  - port_rx_errors
  - port_tx_errors
  - port_rx_frame_err
  - port_rx_over_err
  - port_rx_crc_err
  - port_collisions

</details>

Laplacian correction (adding 1 to all values) was applied before division transformation to handle division by zero.

## Feature Selection

To address the limitations of individual feature selection methods, three methods were employed and the intersection of their results was used to identify key variables. The three methods applied were:

- **FDR**<sup>[[1]](#references)</sup>: controls for the expected proportion of false rejection of features in multiple significance testing
- **Stepwise Selection**<sup>[[2]](#references)</sup>: an iterative process of adding important features to a null set of features and removing the worst performing features
- **Boruta**<sup>[[3]](#references)</sup>: iteratively removes features that are relatively less statistically significant compared to random probability distribution

The 13 transformed features, as well as the final 5 selected by the above feature selection methods' intersection (bolded) is given below:

| No  | Feature Name            | Equation                                                             |
| --- | ----------------------- | -------------------------------------------------------------------- |
| 1   | ip_bytes_sec            | $`\frac{\text{ip\_bytes}}{\text{ip\_duration}}`$                     |
| 2   | **ip_packets_sec**      | $`\frac{\text{ip\_packet}}{\text{ip\_duration}}`$                    |
| 3   | ip_bytes_packet         | $`\frac{\text{ip\_bytes}}{\text{ip\_packet}}`$                       |
| 4   | port_bytes_sec          | $`\frac{\text{port\_bytes}}{\text{ip\_duration}}`$                   |
| 5   | port_packet_sec         | $`\frac{\text{port\_packet}}{\text{ip\_duration}}`$                  |
| 6   | port_byte_packet        | $`\frac{\text{port\_bytes}}{\text{port\_packet}}`$                   |
| 7   | port_flow_count_sec     | $`\frac{\text{port\_flow\_count}}{\text{ip\_duration}}`$             |
| 8   | table_matched_lookup    | $`\frac{\text{table\_matched\_count}}{\text{table\_lookup\_count}}`$ |
| 9   | table_active_lookup     | $`\frac{\text{table\_active\_count}}{\text{table\_lookup\_count}}`$  |
| 10  | **port_rx_packets_sec** | $`\frac{\text{port\_rx\_packets}}{\text{port\_duration\_sec}}`$      |
| 11  | **port_tx_packets_sec** | $`\frac{\text{port\_tx\_packets}}{\text{port\_duration\_sec}}`$      |
| 12  | **port_rx_bytes_sec**   | $`\frac{\text{port\_rx\_bytes}}{\text{port\_duration\_sec}}`$        |
| 13  | **port_tx_bytes_sec**   | $`\frac{\text{port\_tx\_bytes}}{\text{port\_duration\_sec}}`$        |

## Scaling

RobustScaler<sup>[[9]](#references)</sup> (RS) was then applied to handle outliers in the dataset, ensuring that the model is not overly affected by extreme values.

## Dimensionality Reduction

After performing [Model Training & Analysis](/Model%20Training%20&%20Analysis/), the PCA, LDA and ICA dimensionality reduction techniques were then compared using the selected RF model.

<details>

<summary> Comparison of Dimensionality Reduction techniques (click to expand) </summary>

![rf_dim_red](https://github.com/user-attachments/assets/63ab75d8-b090-40d6-b55c-8ed5021e49a5)

</details>

The performance with LDA, the best of all three, was slightly lower than using the dataset without dimensionality reduction. Given that this performance difference is negligible, we opted to use LDA for dimensionality reduction, as it allows us to reduce the feature space from 5 to 4 features.

The final RF model pipeline, with manual division transformation, feature selection through intersection, scaling and dimensionality reduction, gave a final performance of 99.99% across all metrics, with marginal variance.

## References

[1] Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. Journal of the Royal Statistical Society: Series B (Methodological), 57, 289–300.

[2] Naser, M. (2021). Mapping functions: A physics-guided, data-driven and algorithm-agnostic machine learning approach to discover causal and descriptive expressions of engineering phenomena. Measurement, 185, 110098.

[3] Kursa, M. B., & Rudnicki, W. R. (2010). Feature Selection with the Boruta Package. Journal of Statistical Software, 36, 1–13.
