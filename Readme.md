# Healthcare Management API

A lightweight Django REST Framework API for managing patients, doctors, and patient-doctor assignments with JWT authentication.

### Key Design Decisions

- **Authentication & User Model:** The assignment didn't specify a custom user model, so I used Django’s built-in `User` model (`django.contrib.auth.models.User`). It handles secure password hashing and integrates directly with `simplejwt`
    
- **APIView vs. ModelViewSet:** I intentionally implemented `Patient` with `APIView` and `Doctor`/`Mapping` with `ModelViewSet` to compare the two approaches hands-on. `ModelViewSet` is the idiomatic choice for CRUD resources and reduces the ownership-scoping surface (one `get_queryset` vs five hand-written checks). In a production codebase I would standardize on `ModelViewSet` for all CRUD resources and reserve `APIView` for non-CRUD endpoints (auth, webhooks, custom aggregations).
    
- **Doctor Ownership & Access Control:** The spec doesn't specify ownership for doctors. I chose open-to-authenticated for reads because doctors are typically a shared organizational resource — multiple users may need to see the same doctor. I kept `DELETE` open to authenticated as well per spec, but flagged this as a product risk: any authenticated user can delete a doctor, so this is  a known limitation rather than an oversight
    
- **Patient Ownership:** Patients are strictly scoped to the user who created them (`created_by`). Users can only view, edit, or delete their own patient records