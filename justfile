# Task runner for the lemonfiber/brand repo. `just` with no argument lists tasks.
default:
    @just --list

# Turn on the repository's own git hooks. Once per clone.
#
# This repository carries `.githooks/` and nothing switched it on: no recipe, no
# npm `prepare`, no Composer hook, so `core.hooksPath` was never set in any clone
# and the hooks sat there unread. It is per-clone local config and no commit can
# carry it, so it hangs on a command somebody was going to run anyway — `ci`
# depends on this, so running the checks once turns the hooks on for good.
hooks:
    git config core.hooksPath .githooks
    @echo "hooks on: .githooks/commit-msg, .githooks/pre-push"

# The token gate, and the script that decides it — the whole of what CI reads in
# this tree.
#
# It is not CI and does not say it is. Everything else a pull request here starts
# is forge-side, and these are not here:
#
#   commitlint, dco, attribution,   `.githooks/commit-msg` refuses all four
#   the citation gate               before the push, and `hooks` turns it on
#   hygiene                         actionlint, typos, links, markdown, the
#                                   invite check and shared-files — `typos` and
#                                   `lychee --no-progress .` are the two of them
#                                   a clone can run without a spec checkout
#   pins, workflow-pins             ask the forge which commits a pin has not
#                                   taken
#   CodeQL, gitleaks, osv-scanner,  forge-side, and none of them decides
#   sonar, label                    anything about a token
ci: hooks lint tokens

# The gate script itself. First: a name that does not exist here reads as a
# token that does not match.
lint:
    uvx ruff@0.16.4 check scripts/

# Parity between the two token sets, and the contrast arithmetic that decides
# whether a pairing is readable — the self-test before the arithmetic, because a
# wrong answer here ships a colour nobody can read while reporting AA.
tokens:
    python3 scripts/check_tokens.py --self-test
    python3 scripts/check_tokens.py

# The images Home Assistant shows for an integration, rendered from the marks:
# the primary mark as the square icon and the horizontal lockup as the logo, each
# at the size Home Assistant asks for and at twice it. The renderer is pinned, so
# the same marks render the same bytes and every copy can be held to these by
# digest.
export-home-assistant:
    #!/usr/bin/env sh
    set -eu
    render="npx --yes @resvg/resvg-js-cli@2.6.2-beta.1 --no-system-font"
    out=assets/logo/export/home-assistant
    mkdir -p "$out"
    $render --fit-width 256 assets/logo/mark-primary.svg "$out/icon.png"
    $render --fit-width 512 assets/logo/mark-primary.svg "$out/icon@2x.png"
    $render --fit-height 256 assets/logo/lockup-horizontal.svg "$out/logo.png"
    $render --fit-height 512 assets/logo/lockup-horizontal.svg "$out/logo@2x.png"
