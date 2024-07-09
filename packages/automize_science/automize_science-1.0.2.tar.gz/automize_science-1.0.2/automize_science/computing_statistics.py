import pandas as pd
import scipy.stats as stats


def statistics_tests(df_clean, control_name):
    """
    Performs statistical tests on cleaned lipid data to check for normality and equality of variances.

    This function performs the Shapiro-Wilk test for normality of residuals and Levene's test for equality
    of variances between control and experimental groups for each combination of region and lipid.
    """

    regions = []
    lipids = []
    shapiro_normality = []
    levene_equality = []

    print("Checking for the normality of the residuals and the equality of the variances")

    # Test for the normality of the residuals and for the equality of variances
    for (region, lipid), data in df_clean.groupby(["Regions", "Lipids"]):
        control_group = data[data["Genotype"] == control_name]
        experimental_group = data[data["Genotype"] != control_name]
        values = data["Normalized Values"]
        shapiro_test = stats.shapiro(values)
        control_data = control_group["Normalized Values"]
        experimental_data = experimental_group["Normalized Values"]
        levene = stats.levene(control_data, experimental_data)

        shapiro_normality.append(shapiro_test.pvalue)
        levene_equality.append(levene.pvalue)
        regions.append(region)
        lipids.append(lipid)

    # Creating a new dataframe with the normality and equality information
    statistics = pd.DataFrame(
        {
            "Regions": regions,
            "Lipids": lipids,
            "Shapiro Normality": shapiro_normality,
            "Levene Equality": levene_equality,
        }
    )

    return statistics


def z_scores(df_clean, statistics):
    """
    Performs statistical tests to check for normality of residuals and equality of variances.

    This function:
    1. Tests the normality of the residuals using the Shapiro-Wilk test.
    2. Tests the equality of variances using Levene's test.
    3. Compiles the results of these tests for each region and lipid.
    """

    print("Computing the Z scores and the average Z scores per lipid class")

    # Z Scores and average Z Scores per lipid class
    grouped = df_clean.groupby(["Regions", "Lipids"])["Normalized Values"].agg(["mean", "std"]).reset_index()
    grouped.rename(columns={"mean": "Mean", "std": "STD"}, inplace=True)
    df_final = pd.merge(df_clean, grouped, on=["Regions", "Lipids"], how="left")
    df_final["Z Scores"] = (df_final["Normalized Values"] - df_final["Mean"]) / df_final["STD"]
    average_z_scores = (
        df_final.groupby(["Regions", "Lipid Class", "Mouse ID"])["Z Scores"].mean().reset_index(name="Average Z Scores")
    )
    df_final = pd.merge(df_final, average_z_scores, on=["Lipid Class", "Regions", "Mouse ID"])
    df_final = pd.merge(df_final, statistics, on=["Regions", "Lipids"], how="left")

    return df_final
