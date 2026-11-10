# Nexus event/audit coding lab



## Nexus coding lab: start here


### Who works together

Work individually, in pairs, or in ad hoc groups of 2-3 formed from the people present. No Beacon, Atlas or other standing-team membership is required. One working computer per group is enough. Share a saved copy of code and evidence with every contributor before leaving. All three writeup assignments remain individual submissions. Shared code and test results may be used with attribution, but each student writes their own analysis, conclusions and reflection.


### The actual starting point

The starter includes the unchanged nexus2 source and tests from CS5320/project-nexus-atlas at commit 75a8d145aa5bc0c92725197c0e4e9883491c542f. CustomerLifecycleService publishes the trimmed reason in customer.deactivated. CustomerNotificationSubscriber copies it into the simulated customer message. The NEW teaching requirement treats the reason as internal information. The baseline was not previously subject to that policy.


### Codespaces: recommended classroom setup

1. Sign in to GitHub. **Fork** this repository to your own account so your commits go to your copy.
2. On your fork, select **Code → Codespaces → Create codespace on main**. Use the smallest available machine.
3. Wait for setup to finish. The included configuration supplies Python 3.12, the Python editor extension, and installs the project and pytest.
4. Open **Terminal → New Terminal**. From the repository root, run:

```bash
cd nexus2
python run_lab.py
```

Expect **four passes and four failures** on the untouched starter. These failures are the work of the lab, not a Codespaces setup failure. There is no web app to launch, port to forward, database to configure, or local Python installation needed.

The original regression suite is separate:

```bash
python -m pytest tests
```

It initially has 23 passing tests. As you implement the new requirement, update the one notification-message expectation authorized below. Do not delete unrelated checks.

If dependency installation fails, the core `python run_lab.py` command still needs only Python. For the original suite, retry `python -m pip install --user -e ".[dev]"` from `nexus2`. If your Codespace predates this configuration, save your files, fetch the updated configuration into your fork, then run **Codespaces: Rebuild Container** from the Command Palette.

**Groups:** one student can host the working Codespace and share their screen while partners trace, design and test. A Codespace is not automatically a shared editing session. Rotate participation and give every contributor access to the saved code and results. All writeups remain individual.

**Before leaving:** save files, record actual output in the root `evidence.md`, and commit/push to your own fork using Source Control. Check that the remote belongs to your account before pushing. Share the fork link with your partners; no pull request to the class starter is required. Stop the Codespace from [Your Codespaces](https://github.com/codespaces) and reopen that same Codespace Thursday. Closing the browser tab does not stop it. Do not delete it until your work is safely pushed or downloaded.

Codespaces availability depends on your account's allowance and any organization restrictions. If creation is blocked, join a partner's working environment or use the local setup below.

### Local setup: no dependency installation for the core lab

Clone this repository, then run the lab from its `nexus2` directory:

```bash
git clone https://github.com/CS5320/Nexus_Coding_Lab.git
cd Nexus_Coding_Lab/nexus2
python --version
python run_lab.py
```

Alternatively, choose **Code → Download ZIP**, extract it, and open a terminal in the extracted repository's `nexus2` directory.

Use Python 3.11 or newer. On macOS/Linux, use python3 if needed. On Windows, use py -3.11 or another installed 3.11+ interpreter. The runner sets its local import paths. No pip install, web server, database or external email account is needed.


### Expected first result

The supplied eight contract checks initially produce 4 passes and 4 failures. Tests 01, 02, 03 and 08 fail because the new information-flow/audit behavior is absent. This is an expected starting result. Save the command and output in evidence.md before editing. An import error or a missing interpreter is a setup problem, not one of the expected failures.


### If setup or attendance is a problem

Join a working ad hoc group and contribute to design, code tracing and tests. Change who types during the implementation block. For independent work later, clone or download this repository and use these instructions. If you remain blocked, record the attempted command and actual error. Do not claim a successful run. The instructor can help you continue from a working environment.


## The change you must implement


### Required behavior

R1. Preserve current command authorization: admin and manager are allowed; viewer is denied. Preserve missing-customer behavior and the existing minimum of five characters after reason.strip(). Rejected commands must not mutate, publish, notify or write a successful-deactivation audit entry.

R2. A successful deactivation still returns the customer and leaves active=False. The public customer.deactivated event retains customer identity and email but contains no reason or confidential reason text, including under another field name.

R3. The notification message becomes exactly: **Your Atlas account has been deactivated.** The simulated destination email remains unchanged.

R4. Retain exactly one internal audit entry per accepted invocation with customer_id, actor_id and the trimmed reason. Choose its owner and interface. Keep it outside the public EventBus and customer notification path.

R5. Preserve current notification-failure behavior: its exception propagates, the customer stays inactive, and the audit entry must already be available in the current process. Do not redesign retries or delivery recovery.


### What you choose

Choose where the internal audit record lives, how the lifecycle service writes it, and how to wire the dependency. A direct audit collaborator, a service-owned record or a separate private channel may be defensible. Explain a real benefit and cost. A private label on a subscriber of the same public broadcast does not satisfy R2/R4.


### Scope and honest limits

This is an in-process prototype. The audit storage may be in memory; no audit read API, new user roles, database, encryption, durable delivery or deployment is required. Assume the audit write succeeds for this lab. Audit-write failure, concurrency, repeat-request deduplication and crash recovery are outside scope. A private Python field is not production access control. State these limits in your defense.


## Editing, checking and saving


### Files to inspect and change

Start with src/northstar/services.py (CustomerLifecycleService), events.py (DomainEvent/EventBus), notifications.py, and tests/test_lifecycle_service.py. Edit the lifecycle/notification code and add an audit module if useful. You may adapt constructor wiring in tests/conftest.py when your design needs it. Keep unrelated registration, reporting and legacy behavior.


### The lab adapter

lab/adapter.py wires one active customer, a lifecycle service, bus and simulated notification client. Change build() to wire your design. audit_records(system) must return real records produced by your code as mappings with customer_id, actor_id and reason; it may convert your own record type. It must not fabricate records or fix behavior on behalf of production code. Keep the supplied eight checks intact.


### One deliberate upstream test update

The original test_deactivate_sends_notification expects the old reason-bearing message. Change only that message expectation to the generic text in R3, and explain the requirement change in evidence.md. Do not delete tests to hide defects. If pytest is installed, run `python -m pytest tests` from nexus2. Otherwise the core lab remains runnable; mark the full suite unrun. Optional setup: create a virtual environment and install the project with `python -m pip install -e ".[dev]"`.


### Add one behavior check

Add one test method to lab/test_contract.py. Choose a meaningful case such as a five-character trimmed reason, a second public subscriber that must not receive the secret, or two customer deactivations with correctly associated audit entries. State the expected behavior first. Do not merely assert a class name or copy an existing check. Run the suite again and record the actual result.


### Evidence to retain

Use evidence.md: contributors and roles, starting result, ownership choice and alternative, changed files and sanctioned test update, your added check, final command/output, remaining failures and limits. Save source and tests too. Use a ZIP, local copy or accessible branch; no shared-repository push is required. Failed attempts remain useful evidence when accurately explained.


## Class timing and assessment handoff


### Tuesday, November 10: 75 minutes

3:05–3:18: inspect the actual path and changed contract. 3:18–3:25: setup and baseline run. 3:25–3:33: ownership decision. 3:33–3:58: code changes. 3:58–4:03: upstream test conflict. 4:03–4:13: add and run a check. 4:13–4:20: save evidence and individual judgment. All times p.m. Work may continue Thursday.


### Thursday, November 12: 75 minutes

3:05–3:10: regroup and open saved work. 3:10–3:35: finish coding and verification. 3:35–3:44: interpret results and prepare the record. 3:44–4:09: individual PR4 drafting. 4:09–4:17: revision. 4:17–4:20: assessment handoff. All times p.m. The old all-writing workshop and diagnostic-access worksheet are superseded.


### PR4: review response, 25 points

Individual Canvas Text Entry due Friday Nov 13 at 11:59 p.m. Mountain. Five sections: initial claim, actual code/execution evidence and limit, consequential challenge, disposition with cost/risk, next check. Use actual lab evidence or comparable earlier Nexus implementation work. An incomplete or failed attempt is valid to analyze. Each student writes their own judgment.


### DA4: technical defense, 100 points

Individual PDF due Saturday Nov 14 at 11:59 p.m. Mountain. Keep the existing design explanation, alternatives and tradeoffs. Include inspectable changed code/diff and actual output in a short PDF appendix, or an instructor-accessible code/evidence link. Explain which parts are implemented, incomplete or still proposed. No separate upload type is required. Passing every test is not a gate to credit. The existing graduate research appendix remains.


### Portfolio4: learning, 20 points

Update the existing Google Doc and submit its link by Saturday Nov 14 at 11:59 p.m. Mountain. The initial lab design note and current code/test result can be the earlier/current artifacts. Explain what changed or became more precise in your judgment. Existing graduate reflection remains. No submission is due at either class end; the lab evidence sheet is not a fourth graded assignment.
