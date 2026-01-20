#!/bin/bash
# Automated setup script for gym-proj3

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo -e "${GREEN}"
echo "╔════════════════════════════════════════╗"
echo "║  Setting up gym-proj3              ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Backend setup
print_info "Setting up backend..."

if [[ -d "backend" ]]; then
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [[ ! -d "venv" ]]; then
        print_info "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip -q
    
    # Install dependencies
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt -q
    
    # Create necessary directories
    mkdir -p ../databases/seed
    mkdir -p ../databases/runs
    mkdir -p logs
    
    cd ..
    print_success "Backend setup complete"
else
    print_warning "Backend directory not found"
fi

# Frontend setup
print_info "Setting up frontend..."

if [[ -d "frontend" && -f "frontend/package.json" ]]; then
    cd frontend
    
    # Install dependencies
    print_info "Installing Node.js dependencies..."
    npm install --legacy-peer-deps
    
    cd ..
    print_success "Frontend setup complete"
else
    print_warning "Frontend directory or package.json not found"
    print_info "You may need to add UI code to frontend/ directory"
fi

# Create .env file if it doesn't exist
if [[ ! -f ".env" ]]; then
    print_info "Creating .env file..."
    cat > .env <<EOF
# Gym Configuration
GYM_NAME=proj3

# Database
DATABASE_URL=postgresql+psycopg2://proj3:proj3@localhost:5431/postgres
POSTGRES_TEMPLATE_DB=proj3_seed
POSTGRES_RUN_DB_PREFIX=proj3_

# Frontend
NEXT_PUBLIC_API_BASE_PATH=http://localhost:8880
NEXT_PUBLIC_ENABLE_INSTRUMENTATION=false

# Backend
FRONTEND_URL=http://localhost:5173
EOF
    print_success ".env file created"
fi

echo ""
print_success "Setup complete!"
echo ""
print_info "Next steps:"
echo "  1. Review and customize gym.config.json"
echo "  2. Add UI code to frontend/ if not already done"
echo "  3. Start services: docker-compose up -d"
echo "  4. Or run locally:"
echo "     - Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "     - Frontend: cd frontend && npm run dev"
echo ""


