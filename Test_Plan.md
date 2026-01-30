# Front-End Banking System – Test Plan

## 1. Purpose
This document describes the organization and execution of front-end requirements tests.

## 2. Assumptions
- Text-based interface
- Input via standard input
- Known test account:
  - Account: 123456
  - PIN: 4321
  - Balance: $1000

## 3. Test Organization
Tests are organized by functional area:

tests/
├── login/
├── menu/
├── balance/
├── deposit/
├── withdraw/
└── error-handling/

## 4. Test Execution Plan
Tests will be run by redirecting input files into the program and comparing output with expected results using diff.

## 5. Test Run Script
(Include run-tests.sh contents)

## 6. Output Organization
Results will be stored as diff files for later comparison.

## 7. Identified Requirements Issues
- Max login attempts not specified
- Currency formatting unclear
- Error message consistency unspecified
