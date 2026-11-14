# Evaluation Methodology & Closed-Loop Optimization

This guide outlines the empirical, eval-driven methodology for measuring and improving Agent Skills quality.

---

## 1. The Core Testing Pattern

To verify a skill genuinely improves task outcomes, compare outputs using an **A/B Baseline Evaluation**:
- **With Skill**: Run task with the skill loaded in agent context.
- **Without Skill (Baseline)**: Run the exact same task prompt with a generic agent.
- **Metric Delta**: Calculate delta in pass rate, token cost, and execution duration.

---

## 2. Test Suite Architecture (`evals/evals.json`)

A test case has three parts:
1. **Prompt**: Realistic user query (varying from terse to context-heavy).
2. **Expected Output**: Ground-truth description of success.
3. **Assertions**: Verifiable, objective criteria (file existence, specific headers, schema validity).

```json
{
  "skill_name": "csv-cleaner",
  "evals": [
    {
      "id": 1,
      "prompt": "Clean up messy_data.csv and remove blank rows",
      "expected_output": "Cleaned CSV file with headers preserved",
      "assertions": [
        "The output file cleaned_data.csv exists",
        "Row count is greater than 0",
        "No empty rows remain"
      ]
    },
    {
      "id": 2,
      "prompt": "Draft an email to client declining meeting",
      "expected_output": "Handled without csv skill",
      "should_trigger": false
    }
  ]
}
```

---

## 3. Preventing Description Overfitting

When tuning `description` triggers:
- **Train Set (60%)**: Used to identify trigger failures and iterate phrasing.
- **Validation Set (40%)**: Untouched held-out queries to verify generalization.
- Never add verbatim query keywords into the description. Abstract to the general intent category.

---

## 4. Cross-Platform Runner Design
- **Windows Safety**: Avoid Unix `select.select()` on pipes (which causes `WinError 10038` on Windows).
- **Process Management**: Use `subprocess.run()` with explicit `timeout` parameters, or standard thread-safe queues.
- **Outputs**: Output structured `grading.json` for CI/CD assertions and generate static HTML reports for human visual review.
