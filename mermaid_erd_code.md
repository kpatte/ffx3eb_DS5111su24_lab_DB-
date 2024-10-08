```mermaid
erDiagram
    COURSES ||--o{ COURSE_OFFERINGS : "has"
    COURSES ||--o{ LEARNING_OUTCOMES : "has"
    INSTRUCTORS ||--o{ COURSE_OFFERINGS : "teaches"
    TERMS ||--o{ COURSE_OFFERINGS : "includes"
    
    COURSES {
        string course_id PK
        string course_name
        string course_description
        boolean course_active
    }
    
    INSTRUCTORS {
        string instructor_id PK
        string instructor_name
        boolean instructor_active
    }
    
    TERMS {
        string term_id PK
        string term_name
    }
    
    LEARNING_OUTCOMES {
        string outcome_id PK
        string course_id FK
        string learning_outcome_description
    }
    
    COURSE_OFFERINGS {
        string offering_id PK
        string course_id FK
        string term_id FK
        string instructor_id FK
    }
```
