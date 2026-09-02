# GitHub namespace migration

**Status:** PLANNED · NOT YET EXECUTED

## Objective

Migrate the personal GitHub namespace from `ozesnoso0903-cyber` to the approved public identity while preserving repository continuity and updating explicit references that would otherwise break or become stale.

## Identity model

- Human subject: Salvador Osorio
- Authored/social signature: SOA
- Technical architecture/program: SOAiaCore
- Preferred personal GitHub username: `salvador-osorio`, subject to final GitHub availability at execution time

## Known explicit references to the old namespace

### Profile repository

The current special profile repository is named exactly like the current username. After the account username changes, the profile repository must be renamed to match the new username so GitHub continues to render its README as the profile README.

Historical references to the current username exist in the legacy public README and in obsolete Pages/Jekyll files already scheduled for removal by the sanitation pass.

### Cross-repository references

1. `SOAIACORE-Corporation/policy-continuidad/.github/CODEOWNERS`
   - references `@ozesnoso0903-cyber`
   - must be updated immediately after the account rename

2. `SOAIACORE-Corporation/demo-repository/.github/workflows/auto-assign.yml`
   - assigns issues to `ozesnoso0903-cyber`
   - must be updated immediately after the account rename

## Registry / package namespace

Repository code search found no indexed references to `ghcr.io/ozesnoso0903-cyber`. This is not equivalent to a complete GitHub Packages / GHCR inventory. Registry ownership, image consumers and infrastructure bindings must be verified separately before or immediately after the namespace migration.

## Execution sequence

1. Close or adjudicate Gate A.
2. Merge the sanitation PR.
3. Merge the public-identity/licensing PR.
4. Verify the target username is available in GitHub at execution time.
5. Change the GitHub account username.
6. Rename the special profile repository to exactly match the new username.
7. Update CODEOWNERS and workflow assignee references in the two known organization repositories.
8. Update local Git remotes, deployment references, badges and external links that still use the old namespace.
9. Verify GHCR / Packages ownership and all image consumers.
10. Validate the profile README, repository redirects and canonical `soaiacore.com` links.
11. Record a migration receipt with old namespace, new namespace, affected repositories and final verification state.

## Safety rule

Do not pre-change CODEOWNERS or assignee references to the new username before the account rename; the target principal must exist first. The account rename and dependent reference updates should be treated as one controlled migration window.
