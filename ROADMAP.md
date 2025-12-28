# Roadmap

This document outlines the planned evolution of the public reference repo versus the private product.

## Public Repo (This Repository)

**Focus:** Stable reference implementation, documentation, and learning resource.

**Planned:**
- ✅ Initial release with CLI + Streamlit UI
- ✅ Core pipeline with compliance checking
- ✅ Provider abstraction (Mock + OpenAI)
- ✅ Token budgeting and metadata tracking
- 🔄 Keep spec→artifacts contract stable
- 🔄 Small UX improvements to Streamlit UI
- 🔄 Enhanced quality/compliance reports
- 🔄 Template scaffolding (if useful for community)
- 🔄 Additional example specs

**Not Planned (Private Product Only):**
- User authentication/accounts
- Persistent storage or run history
- RAG (Retrieval-Augmented Generation)
- Multi-pass optimization loops
- Analytics and usage tracking
- Production SLOs/monitoring
- Billing or subscription features

## Private Product (Separate Repository)

**Focus:** Production service with reliability, optimization, and enterprise features.

**Planned:**
- Authentication and user management
- Persistent run history and storage
- RAG integration for facts mode (sources + citations)
- Multi-pass optimizers and revision loops
- Analytics dashboard and usage metrics
- Production hardening (SLOs, monitoring, alerting)
- Billing and subscription management
- Enterprise features (SSO, audit logs, etc.)

**Architecture Note:**
The private product will reuse the core engine interfaces from this public repo, but add proprietary layers for storage, optimization, and reliability. The spec→artifacts contract remains stable across both.

