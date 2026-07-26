# Connecting GitHub MCP to Claude Code

**Goal:** register GitHub's hosted MCP server so Claude Code can work with your repos, issues, and PRs.

**Status:** connected and verified (authenticated as `vsanand27`).

## Steps

1. **Create a GitHub token** — a fine-grained PAT at <https://github.com/settings/personal-access-tokens> with these repository permissions:
   - Contents — Read/Write
   - Pull requests — Read/Write
   - Issues — Read/Write
   - Metadata — Read (granted automatically)
2. **Open a real PowerShell window** (Win → type "PowerShell" → Enter). Not Claude Code's bash mode, not cmd.
3. **Add the server** — two lines, run one at a time:
   ```powershell
   $t = "your_token_here"
   claude mcp add --scope user --transport http github "https://api.githubcopilot.com/mcp/" --header "Authorization: Bearer $t"
   ```
4. **Verify:**
   ```powershell
   claude mcp list
   ```
   Look for: `github: ... - ✔ Connected`
5. **Restart Claude Code** — MCP tools load at session startup, so they only become usable in a fresh session.

## Key gotchas

- **Never paste your token into the Claude Code chat.** It gets saved in the transcript and is instantly compromised. Run token commands in a separate terminal.
- **Use real PowerShell, not Git Bash or cmd.** Claude Code's bash mode doesn't expand `$env:...` / `$t`, so the literal text gets stored as your "token" → `HTTP 400: invalid token`.
- **Keep the `claude mcp add` command on one line.** A paste that breaks after `github` makes PowerShell try to run the URL as a command. Quoting the URL guards against this.
- **OAuth doesn't work here.** GitHub's endpoint rejects Claude Code's OAuth flow (no dynamic client registration support), so the token header is the way.
- **`--scope user`** makes it available in all projects. Use `--scope project` instead to check it into a repo's `.mcp.json`.

## Rotating or removing the token

```powershell
claude mcp remove --scope user github
# then re-run the add command with the new token
```
