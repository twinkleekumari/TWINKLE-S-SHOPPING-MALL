# Project Statement: Retail Billing & Invoice System

## 1. Problem Statement
Small-to-medium retail outlets and point-of-sale (POS) terminals often require an efficient, lightweight, and interactive terminal application to manage customer check-ins, dynamic cart generation, accurate tax calculations, and versatile payment processing. Many existing solutions are either overly complex or lack built-in capabilities for real-time item consolidation and digital invoice delivery (e.g., email receipts).

This project provides a modular, reliable Python CLI solution designed to streamline the in-store billing workflow, ensure robust data entry validation, and support both physical (receipt printing) and digital (SMTP email) customer deliverables.

---

## 2. Project Objectives
- **Automated Customer CRM Check-In**: Quick lookup by 10-digit phone number with seamless new user registration.
- **Dynamic Cart Management**: Interactive product addition with automated quantity consolidation for duplicate items.
- **Accurate Financial Calculations**: Automated calculation of line-item totals, dynamic tax application, subtotaling, and grand total computation.
- **Multi-Modal Payment Handling**: Processing support for Cash (including automatic change computation), Card, and online/UPI transactions.
- **Digital Invoicing**: Plain-text monospaced receipt generation and optional automated email dispatch via SMTP.
- **Maintainability & Testability**: Modular code architecture backed by comprehensive unit testing (`unittest`).

---

## 3. Scope of Work

### In-Scope
- Command-line interface (CLI) for cashier/user interactions.
- Customer record management in-memory (extensible to databases).
- Input validation for phone numbers, email addresses, product IDs, quantities, and cash inputs.
- Invoice generation and formatted receipt rendering.
- E-mail notification system using TLS/SMTP.

### Out-of-Scope (Future Enhancements)
- Graphical User Interface (GUI) or Web Dashboard.
- Hardware-level POS integration (e.g., thermal printer drivers, barcode scanner input).
- Persistent relational database connection (SQLite/PostgreSQL integration planned for future iterations).

---

## 4. Key Functional Requirements

1. **Input Validation**:
   - Phone numbers must consist of exactly 10 numeric digits.
   - Email addresses must conform to standard RFC email patterns.
   - Cash payments must meet or exceed the grand total.

2. **Cart Consolidation**:
   - Adding a product ID already present in the active cart must increment its existing quantity rather than creating duplicate line items.

3. **Receipt Formatting**:
   - All receipts must be rendered in fixed-width monospaced columns with accurate floating-point currency formatting (`$XX.XX`).