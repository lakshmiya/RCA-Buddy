#!/bin/bash

INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ "$TOOL_NAME" = "runTerminalCommand" ]; then
    if echo "$TOOL_INPUT" | grep -qE 'rm[[:space:]]+-rf|DROP[[:space:]]+TABLE|DELETE[[:space:]]+FROM|TRUNCATE[[:space:]]+TABLE'; then
        echo '{"hookSpecificOutput":{"permissionDecision":"deny","permissionDecisionReason":"Destructive command blocked by RCA Buddy security policy."}}'
        exit 0
    fi
fi

echo '{"continue":true}'
