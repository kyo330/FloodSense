def simulate_risk(infra_df, rainfall):
    """
    Estimate risk level for infrastructure based on rainfall and age.
    """
    risk_levels = []
    recommendations = []

    for _, row in infra_df.iterrows():
        age_factor = row['age'] / 50
        rainfall_factor = rainfall / 100
        risk_score = (0.6 * rainfall_factor) + (0.4 * age_factor)

        if risk_score < 0.5:
            risk_level = "Low"
            recommendation = "Monitor only"
        elif 0.5 <= risk_score < 0.8:
            risk_level = "Moderate"
            recommendation = "Prepare boil water notice"
        else:
            risk_level = "High"
            recommendation = "Issue boil water notice"

        risk_levels.append(risk_level)
        recommendations.append(recommendation)

    infra_df = infra_df.copy()
    infra_df["rainfall"] = rainfall
    infra_df["risk_level"] = risk_levels
    infra_df["recommendation"] = recommendations
    return infra_df
