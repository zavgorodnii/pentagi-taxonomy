#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Pentagi Taxonomy GitHub Installation Test${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source test_venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Testing Version 1${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Install v1 from GitHub
echo -e "${BLUE}Installing pentagi-taxonomy v1 from GitHub...${NC}"
pip install "git+https://github.com/zavgorodnii/pentagi-taxonomy.git#subdirectory=v1/python"

# Run v1 tests
echo ""
echo -e "${BLUE}Running v1 tests...${NC}"
python test_v1.py

# Uninstall v1
echo ""
echo -e "${BLUE}Uninstalling v1...${NC}"
pip uninstall -y pentagi-taxonomy

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Testing Version 2${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Install v2 from GitHub
echo -e "${BLUE}Installing pentagi-taxonomy v2 from GitHub...${NC}"
pip install "git+https://github.com/zavgorodnii/pentagi-taxonomy.git#subdirectory=v2/python"

# Run v2 tests
echo ""
echo -e "${BLUE}Running v2 tests...${NC}"
python test_v2.py

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ All tests completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Both Version 1 and Version 2 were successfully:"
echo "  1. Installed from GitHub"
echo "  2. Imported in Python code"
echo "  3. Used to create and validate entities"
echo ""
echo "This confirms that the README installation instructions work correctly!"

