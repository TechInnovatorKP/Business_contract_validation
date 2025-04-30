import re

def validate_contract(text, contract_type=None):  # Accept contract_type as optional param
    lines = text.split('\n')
    clause_pattern = re.compile(r'^\d+\.\s+')
    clauses = [line.strip() for line in lines if clause_pattern.match(line.strip())]

    num_clauses = len(clauses)

    detailed_analysis = []
    high_risk = []
    needs_changes = []
    risk_distribution = {
        "low": 0,
        "medium": 0,
        "high": 0
    }

    for clause in clauses:
        risk_level = "low"
        suggestion = "No issues detected."

        # Customize based on contract type
        clause_lower = clause.lower()

        if "termination" in clause_lower or "liability" in clause_lower:
            risk_level = "high"
            suggestion = "Review this clause thoroughly. It may have significant legal or financial implications. Consider legal consultation."
            high_risk.append(clause)
            needs_changes.append(clause)
        elif "confidentiality" in clause_lower or "payment" in clause_lower:
            risk_level = "medium"
            suggestion = "This clause should be reviewed for clarity and mutual obligations."
            if "confidentiality" in clause_lower:
                needs_changes.append(clause)
        else:
            risk_level = "low"
            suggestion = "No major issues, but double-check for completeness."

        # Example: adjust risk for affiliate contracts
        if contract_type and contract_type.lower() == "affiliate":
            if "commission" in clause_lower:
                risk_level = "medium"
                suggestion = "Ensure commission structure is clearly defined."
                needs_changes.append(clause)

        risk_distribution[risk_level] += 1

        detailed_analysis.append({
            "clause": clause,
            "risk_level": risk_level.capitalize(),
            "suggestion": suggestion
        })

    return {
        "num_clauses": num_clauses,
        "num_risky_clauses": len(high_risk),
        "high_risk_clauses": high_risk,
        "clauses_needing_changes": needs_changes,
        "risk_distribution": risk_distribution,
        "detailed_analysis": detailed_analysis
    }