# 🔄 SnapStack Development Workflow

## 📋 Daily Development Process

### 1. Start Your Day
```bash
# Pull latest changes
git pull origin master

# Check GitHub Project Board
# https://github.com/latitudeki5223/snapstack/projects

# Review assigned issues
gh issue list --assignee @me
```

### 2. Pick a Task
- Check "Current Sprint" column in project board
- Choose task based on priority (🔴 > 🟡 > 🟢)
- Assign yourself and move to "In Progress"

### 3. Create Feature Branch
```bash
# Branch naming convention
git checkout -b <type>/<ticket>-<description>

# Examples:
git checkout -b feat/12-sovrn-api-integration
git checkout -b fix/23-parser-accuracy
git checkout -b docs/34-api-documentation
```

### 4. Development
```bash
# Start development environment
./start-admin.sh  # For admin work
turbo dev         # For everything

# Make changes
# Write tests (when applicable)
# Update documentation
```

### 5. Pre-Commit Checks
```bash
# Run quality checks
bin/verify

# Run specific tests
turbo test --filter=parser

# Manual testing
# - Test your feature thoroughly
# - Check for regressions
```

### 6. Commit Changes
```bash
# Stage changes
git add .

# Commit with conventional format
git commit -m "<type>(<scope>): <description>"

# Commit types:
# feat:     New feature
# fix:      Bug fix
# docs:     Documentation
# style:    Formatting, no code change
# refactor: Code restructuring
# test:     Adding tests
# chore:    Maintenance

# Examples:
git commit -m "feat(parser): add spaCy NLP layer"
git commit -m "fix(ui): correct mobile layout issue"
git commit -m "docs(api): update endpoint documentation"
```

### 7. Push and Create PR
```bash
# Push branch
git push origin <branch-name>

# Create PR with GitHub CLI
gh pr create \
  --title "feat: Add Sovrn API integration" \
  --body "Closes #12" \
  --label "api,enhancement"

# Or create via GitHub UI
```

### 8. PR Description Template
```markdown
## Description
Brief description of changes

## Related Issue
Closes #[issue-number]

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Done
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No regressions found

## Screenshots (if UI changes)
[Add screenshots]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### 9. Code Review Process
- Request review from team member
- Address feedback promptly
- Re-request review after changes
- Squash and merge when approved

### 10. Post-Merge
```bash
# Switch back to master
git checkout master
git pull origin master

# Delete local branch
git branch -d <branch-name>

# Move issue to "Done" in project board
```

---

## 🌳 Branch Strategy

### Main Branches
- `master` - Production-ready code
- `develop` - Integration branch (optional)

### Feature Branches
- `feat/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation
- `style/*` - Formatting/styling
- `refactor/*` - Code refactoring
- `test/*` - Test additions
- `chore/*` - Maintenance tasks

### Release Process
```bash
# Create release branch
git checkout -b release/v0.1.0

# Update version numbers
# Run final tests
# Create PR to master

# After merge, tag release
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

---

## 🏃 Sprint Workflow

### Sprint Planning (Monday, Week 1)
1. Review backlog
2. Estimate tasks
3. Assign to sprint
4. Update SPRINT_PLAN.md

### Daily Standup (Every morning)
Post in Slack/Discord:
- Yesterday: What I completed
- Today: What I'm working on
- Blockers: Any issues

### Sprint Review (Friday, Week 2)
1. Demo completed features
2. Update PROGRESS.md
3. Close completed issues
4. Archive sprint

### Sprint Retrospective
- What went well?
- What could improve?
- Action items for next sprint

---

## 📊 Project Board Management

### Columns
1. **📋 Backlog** - All unassigned tasks
2. **🎯 Current Sprint** - This sprint's work
3. **🚧 In Progress** - Actively working
4. **👀 In Review** - PR created, needs review
5. **✅ Done** - Completed and merged

### Issue Labels
- **Priority**: `critical`, `high`, `medium`, `low`
- **Type**: `bug`, `enhancement`, `task`, `documentation`
- **Component**: `parser`, `api`, `ui`, `backend`, `mobile`
- **Status**: `blocked`, `needs-review`, `ready`
- **Size**: `xs`, `s`, `m`, `l`, `xl`

---

## 🧪 Testing Standards

### Test Requirements
- Parser: 95% accuracy target
- API: Mock all external calls
- UI: Component tests + snapshots
- Coverage: Minimum 80%

### Running Tests
```bash
# All tests
turbo test

# Specific package
turbo test --filter=parser

# Watch mode
turbo test --filter=parser -- --watch

# Coverage report
turbo test -- --coverage
```

---

## 📝 Documentation Standards

### Code Documentation
- Python: Docstrings for all public functions
- TypeScript: JSDoc for complex functions
- README in each package

### API Documentation
- OpenAPI/Swagger spec
- Example requests/responses
- Error codes documented

### User Documentation
- Update PROJECT_GUIDE.md for architecture changes
- Update relevant README files
- Add inline comments for complex logic

---

## 🚀 Deployment Process

### Development
- Auto-deploy on merge to `develop`
- URL: dev.snapstack.com

### Staging
- Deploy release candidates
- URL: staging.snapstack.com

### Production
- Deploy from `master` only
- Requires approval
- URL: snapstack.com

---

## 🔧 Useful Commands

### Development
```bash
# Start everything
turbo dev

# Start specific app
turbo dev --filter=web

# Clean build artifacts
turbo clean

# Fresh install
rm -rf node_modules package-lock.json
npm install
```

### Git
```bash
# Interactive rebase
git rebase -i HEAD~3

# Amend last commit
git commit --amend

# Reset to remote
git reset --hard origin/master

# Cherry-pick commit
git cherry-pick <commit-hash>
```

### GitHub CLI
```bash
# List issues
gh issue list

# Create issue
gh issue create

# Create PR
gh pr create

# Check PR status
gh pr status

# Review PR
gh pr review
```

---

## 📞 Getting Help

### Resources
- [PROJECT_GUIDE.md](../PROJECT_GUIDE.md) - Architecture and design
- [SPRINT_PLAN.md](./SPRINT_PLAN.md) - Current sprint goals
- [PROGRESS.md](./PROGRESS.md) - Overall progress tracking
- [GitHub Issues](https://github.com/latitudeki5223/snapstack/issues)

### Contact
- GitHub Issues for bugs/features
- Discussions for questions
- Direct message for urgent items

---

## ⚡ Quick Start for New Contributors

1. **Clone the repo**
   ```bash
   git clone https://github.com/latitudeki5223/snapstack.git
   cd snapstack
   ```

2. **Install dependencies**
   ```bash
   npm install
   cd apps/backend && pip install -r requirements.txt
   ```

3. **Start development**
   ```bash
   ./start-admin.sh
   ```

4. **Pick a "good first issue"**
   - Look for `good-first-issue` label
   - Start with documentation or tests

5. **Make your first PR!**

---

*Last updated: January 22, 2024*