#!/bin/bash
# Update .env file with Supabase credentials

ENV_FILE="/Users/franciscocambero/Anitgravity/.env"

# Backup existing .env
cp "$ENV_FILE" "$ENV_FILE.backup"

# Update the .env file
cat > "$ENV_FILE" << 'EOF'
# SUPABASE CONFIGURATION
NEXT_PUBLIC_SUPABASE_URL="https://qkyemdzfnhqwmrfkzgqj.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="sb_publishable_3E8OX_kLQYLeSCg3de7LSw_vzn9B6nH"
SUPABASE_SERVICE_ROLE_KEY="[key]"

# AI/LLM KEYS
OPENAI_API_KEY="[key]"
ANTHROPIC_API_KEY="[key]"

# ENVIRONMENT
NODE_ENV="development"
PYTHON_ENV="development"

# OPTIONAL: THIRD-PARTY INTEGRATIONS
# STRIPE_SECRET_KEY="[key]"
# SENDGRID_API_KEY="[key]"
EOF

echo "✅ .env file updated successfully!"
echo "📋 Updated values:"
echo "  - NEXT_PUBLIC_SUPABASE_URL: https://qkyemdzfnhqwmrfkzgqj.supabase.co"
echo "  - NEXT_PUBLIC_SUPABASE_ANON_KEY: sb_publishable_3E8OX_***"
echo ""
echo "⚠️  Note: SUPABASE_SERVICE_ROLE_KEY still needs to be set manually"
echo "    Get it from: https://supabase.com/dashboard/project/qkyemdzfnhqwmrfkzgqj/settings/api-keys"
echo "    Click 'Reveal' on the service_role key and copy it"
