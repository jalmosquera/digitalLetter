#!/bin/bash
# Linear Helper Script - Bash wrapper for agents
# Simplifies Linear API calls for Claude Code agents

set -e

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

if [ -z "$LINEAR_API_KEY" ]; then
    echo "❌ LINEAR_API_KEY not found in .env"
    exit 1
fi

LINEAR_API_URL="https://api.linear.app/graphql"

# Function to make GraphQL requests
linear_query() {
    local query="$1"
    curl -s -X POST "$LINEAR_API_URL" \
        -H "Authorization: $LINEAR_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\"}"
}

# Search issue by title
search_issue() {
    local title="$1"
    local query="query { issues(filter: { title: { contains: \\\"$title\\\" } }) { nodes { id identifier title state { id name } } } }"
    linear_query "$query"
}

# Update issue state
update_state() {
    local issue_id="$1"
    local state_name="$2"

    # First get state ID
    local states_query="query { workflowStates { nodes { id name } } }"
    local states_response=$(linear_query "$states_query")

    # Extract state ID (simple grep, could be improved with jq)
    # For now, we'll use predefined state IDs or pass them directly

    local mutation="mutation { issueUpdate(id: \\\"$issue_id\\\", input: { stateId: \\\"$state_name\\\" }) { success issue { id identifier state { name } } } }"
    linear_query "$mutation"
}

# Add comment to issue
add_comment() {
    local issue_id="$1"
    local comment="$2"
    local mutation="mutation { commentCreate(input: { issueId: \\\"$issue_id\\\", body: \\\"$comment\\\" }) { success } }"
    linear_query "$mutation"
}

# Main command router
case "$1" in
    search)
        search_issue "$2"
        ;;
    update)
        update_state "$2" "$3"
        ;;
    comment)
        add_comment "$2" "$3"
        ;;
    *)
        echo "Usage: $0 {search|update|comment} [args]"
        exit 1
        ;;
esac
