# GitHub Actions Workflows

## Overview

This directory contains GitHub Actions workflows for automated testing with flexible configuration options.

## Available Workflows

### 1. Run Tests with Tag Input

**File:** `run-tests-with-tag.yml`

**Trigger:** Manual (workflow_dispatch)

**Description:** Run Behave tests with custom tag filtering and generate comprehensive reports.

#### Features

- ✅ **Custom Tag Selection** - Run specific test scenarios by tag
- ✅ **Browser Selection** - Choose chromium, firefox, or webkit
- ✅ **Headless Mode** - Run in headed or headless mode
- ✅ **Dual Reporting** - Generate both HTML and Allure reports
- ✅ **Artifact Upload** - Automatic upload of reports, screenshots, and traces
- ✅ **Smart Detection** - Only uploads artifacts that were actually generated
- ✅ **Detailed Summary** - Rich test summary in workflow results

#### How to Use

1. **Navigate to Actions Tab**
   - Go to your repository on GitHub
   - Click on the "Actions" tab

2. **Select Workflow**
   - Find "Run Tests with Tag Input" in the workflows list
   - Click on it

3. **Run Workflow**
   - Click the "Run workflow" button
   - Fill in the inputs:
     - **Test Tag**: e.g., `@smoke`, `@OV_03`, `@High`, `@SecurityPosture`
     - **Browser**: chromium (default), firefox, or webkit
     - **Headless**: true (default) or false
     - **Generate Reports**: true (default) or false
   - Click "Run workflow"

4. **Monitor Execution**
   - Watch the workflow run in real-time
   - Check the logs for detailed execution information

5. **Download Artifacts**
   - Once complete, scroll to the "Artifacts" section
   - Download the reports you need

#### Inputs

| Input | Description | Required | Default | Type |
|-------|-------------|----------|---------|------|
| `test_tag` | Behave tag to run | Yes | `@smoke` | string |
| `browser` | Browser to use | No | `chromium` | choice |
| `headless` | Run in headless mode | No | `true` | boolean |
| `generate_reports` | Generate HTML and Allure reports | No | `true` | boolean |

#### Outputs (Artifacts)

The workflow generates the following artifacts:

| Artifact | Description | When Generated | Retention |
|----------|-------------|----------------|-----------|
| `html-report-*` | Standalone HTML report | Always (if reports enabled) | 30 days |
| `allure-results-*` | Raw Allure test results | Always (if reports enabled) | 30 days |
| `allure-report-*` | Interactive Allure report | Always (if reports enabled) | 30 days |
| `screenshots-*` | Failure screenshots | Only on test failures | 14 days |
| `traces-*` | Playwright execution traces | Only on test failures | 14 days |

#### Examples

##### Example 1: Run Smoke Tests

```yaml
Inputs:
  test_tag: @smoke
  browser: chromium
  headless: true
  generate_reports: true
```

##### Example 2: Run Specific Test Scenario

```yaml
Inputs:
  test_tag: @OV_03
  browser: chromium
  headless: true
  generate_reports: true
```

##### Example 3: Run High Priority Tests in Firefox

```yaml
Inputs:
  test_tag: @High
  browser: firefox
  headless: true
  generate_reports: true
```

##### Example 4: Debug in Headed Mode

```yaml
Inputs:
  test_tag: @OV_03
  browser: chromium
  headless: false
  generate_reports: true
```

##### Example 5: Run Security Posture Tests

```yaml
Inputs:
  test_tag: @SecurityPosture
  browser: chromium
  headless: true
  generate_reports: true
```

#### Required Secrets

Add these secrets to your repository settings:

| Secret | Description | Example |
|--------|-------------|---------|
| `PORTAL_BASE_URL` | Base URL of the application under test | `https://dev-aisoc-fe.qualgo.dev` |
| `TEST_EMAIL` | Test user email | `test.user@example.com` |
| `TEST_PASSWORD` | Test user password | `SecurePassword123!` |

**To add secrets:**
1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each secret with its value

#### Workflow Steps

1. **Checkout code** - Gets the latest code from repository
2. **Set up Python** - Installs Python 3.11
3. **Cache dependencies** - Caches pip packages for faster runs
4. **Install dependencies** - Installs Python packages from requirements.txt
5. **Install Playwright** - Installs selected browser
6. **Create directories** - Sets up reports directories
7. **Create .env file** - Creates environment configuration
8. **Verify environment** - Displays configuration details
9. **Run tests** - Executes Behave tests with selected tag
10. **Install Allure CLI** - Installs Allure command-line tool
11. **Generate Allure report** - Converts results to HTML report
12. **Check files** - Verifies which artifacts were created
13. **Upload artifacts** - Uploads all generated files
14. **Display summary** - Shows detailed execution summary

#### Troubleshooting

##### Issue: No artifacts uploaded

**Possible causes:**
- Tests didn't run (check test execution step logs)
- No matching tests for the tag (verify tag exists in feature files)
- Secrets not configured (check repository secrets)

**Solution:**
1. Check the "Check generated files" step output
2. Verify your test tag exists: `grep -r "@your_tag" features/`
3. Ensure all required secrets are set
4. Check test execution logs for errors

##### Issue: Tests failed but no screenshots

**Possible causes:**
- SCREENSHOT_ON_FAILURE disabled
- Tests errored before screenshot could be taken

**Solution:**
- Check `config/settings.py` for SCREENSHOT_ON_FAILURE setting
- Review test execution logs for early failures

##### Issue: Allure report not generated

**Possible causes:**
- Allure CLI installation failed
- No test results to process

**Solution:**
1. Check "Install Allure CLI" step logs
2. Verify allure-results contains files
3. Check "Generate Allure report" step logs

#### Best Practices

1. **Tag Organization**
   - Use meaningful tags (@smoke, @regression, @High, @Critical)
   - Combine tags strategically (@SecurityPosture, @validation)
   - Document tags in feature files

2. **Artifact Management**
   - Download artifacts within retention period
   - HTML reports are self-contained (easiest to share)
   - Allure reports require extracting and opening index.html

3. **Debugging**
   - Use headless=false to see browser in action
   - Download traces for detailed debugging
   - Use screenshots to understand failure context

4. **Performance**
   - Use caching to speed up dependency installation
   - Run focused tests with specific tags
   - Adjust retention days based on needs

## Adding More Workflows

To add additional workflows:

1. Create a new `.yml` file in this directory
2. Define the trigger (on: push, pull_request, schedule, etc.)
3. Add necessary jobs and steps
4. Test thoroughly before merging

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Behave Documentation](https://behave.readthedocs.io/)
- [Allure Framework](https://docs.qameta.io/allure/)
- [Playwright Documentation](https://playwright.dev/)

## Support

For issues with workflows:
1. Check workflow run logs
2. Verify secrets are configured
3. Test commands locally first
4. Review this README for troubleshooting tips

