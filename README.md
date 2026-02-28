# code4baddies
# AarogyaPath - HealthTech Platform (Patient and Doctor)

AarogyaPath is a dual-portal healthcare platform built for rural and low-bandwidth environments.  
It includes a mobile-friendly patient web app and a separate doctor dashboard.

## Project Overview
The system is structured around lightweight frontends, an AI-assisted triage engine, secure data handling, and multilingual support.  
The goal is to make healthcare accessible in regions with limited connectivity.

## Features

### Patient Application
- Multilingual interface (12+ supported languages)
- AI-assisted symptom triage
- Voice input and voice output using browser-native Web Speech API
- Access to nearby clinics and pharmacies using Google Maps
- Consultation booking (AI, video, or clinic)
- Prescriptions, vitals and consultation history
- Offline caching using localStorage

### Doctor Portal
- Live patient queue management
- Queue sorted by AI-generated triage level
- Consultation history
- Rating and review system
- Clinic stock tracking and stock-out prediction

## Proposed Solution
The platform breaks down complex healthcare workflows into an accessible, low-bandwidth system.  
It focuses on:
- Lightweight frontends that run smoothly on low-end devices  
- Predictive and AI-assisted decision support  
- Efficient caching and pagination to reduce bandwidth usage  
- Secure and compliant handling of health data  
- Clean separation of patient and doctor features for ease of use  

## Tech Stack

### Frontend
- HTML, CSS, JavaScript  
- Tailwind CSS (via CDN)  
- Web Speech API  
- Google Maps JavaScript SDK  
- Agora Web SDK (for video consultations)

### Backend
- Django 4.2  
- Django REST Framework  
- SimpleJWT authentication  
- PostgreSQL 
- Gemini 1.5 Flash API (AI triage and chat)  
- Google Translate API  



