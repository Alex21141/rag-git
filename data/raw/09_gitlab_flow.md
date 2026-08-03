# GitLab Flow

GitLab Flow is a simplified Git branching strategy that integrates feature-driven development with issue tracking and continuous delivery.

## Why GitLab Flow supports modern development

Git simplifies branching and merging, prompting many software development teams to move away from older source control tools like SVN and adopt Git-based workflows that streamline collaboration.

However, organizations transitioning from traditional version control systems often face challenges identifying a workflow that aligns with their development process.

GitLab Flow addresses this gap by providing a seamless approach to software development. It integrates Git workflows with issue tracking, enabling teams to manage code and collaboration in a unified system.

## GitLab Flow, the GitFlow alternative

GitLab Flow is a simpler alternative to GitFlow and combines feature driven development and feature branches with issue tracking.

With GitLab Flow, all features and fixes go to the `main` branch while enabling `production` and `stable` branches. GitLab Flow includes a set of best practices and guidelines to ensure software development teams follow a smooth process to ship features collaboratively.

By tightly integrating issue tracking into the development workflow, GitLab Flow improves traceability, aligns code changes with business priorities, and supports better collaboration. This structure helps teams avoid the complexity of managing multiple long-lived branches, as seen in GitFlow, while still supporting stable deployments across environments.

## How does GitLab Flow work?

With GitFlow, developers create a `develop` branch and make that the default, while GitLab Flow works with the `main` branch right away. GitLab Flow incorporates a pre-production branch to make bug fixes before merging changes back to `main` before going to production. Teams can add as many pre-production branches as needed — for example, from `main` to test, from test to acceptance, and from acceptance to production.

Essentially, teams practice feature branching, while also maintaining a separate production branch. Whenever the 'main' branch is ready to be deployed, users merge it into the production branch and release. GitLab Flow is often used with release branches. Teams that require a public API may need to maintain different versions. Using GitLab Flow, teams can make a `v1` branch and a `v2` branch that can be maintained individually, which can be helpful if the team identifies a bug during code reviews that goes back to `v1.`

## Key benefits of GitLab Flow

GitLab Flow offers a simple, transparent, and effective way to work with Git. Using GitLab Flow, developers can collaborate on and maintain several versions of software in different environments.

GitLab Flow also decreases the overhead of releasing, tagging, and merging, which is a common challenge encountered with other types of Git workflows, to create an easier way to deploy code. Commits flow downstream to ensure that every line of code is tested in all environments. Teams of any size can use GitLab Flow, and it has the flexibility to adapt to various needs and challenges.

### Key benefits include:

- Streamlined collaboration across teams — GitLab Flow enables developers to work together more efficiently by centralizing work around feature branches and issue tracking, making it easier to maintain multiple versions of software across different environments.
- Reduced overhead in releases — Unlike other Git workflows, GitLab Flow simplifies the process of releasing, tagging, and merging, helping teams deploy code more frequently and with fewer blockers.
- Improved code quality and testing consistency — Commits naturally flow downstream, ensuring that every change is tested consistently across all environments before reaching production.
- Flexibility for teams of any size — Whether you're a small team or a large enterprise, GitLab Flow adapts to diverse workflows and deployment needs without introducing unnecessary complexity.

## GitLab Flow vs GitFlow comparison

| Feature | GitFlow | GitLab Flow |
| --- | --- | --- |
| Default branch | `develop` | `main` |
| Production branch | Optional tag-based releases | Dedicated production branch |
| Pre-production | `develop` branch | Multiple environment branches |
| Release branches | Required for production | Optional for API/versioning |
| Complexity | High (5+ branch types) | Low (main + env branches) |
| Continuous delivery | Difficult | Native support |

## Best practices for GitLab Flow

- Use `main` as the source of truth — all features and fixes go to main
- Create feature branches from `main` — branch as late as possible
- Merge to `main` frequently — keep main deployable at all times
- Use environment branches for pre-production — staging, testing, acceptance
- Protect `main` with merge request requirements — require reviews before merging
- Use issue tracking to scope work — every code change should have a reason
- Keep feature branches small and short-lived — merge often to minimize conflicts
