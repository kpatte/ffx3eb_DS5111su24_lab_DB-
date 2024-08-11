-- 1) Which courses are currently included (active) in the program?
SELECT course_id AS course_mnemonic, course_name
FROM courses
WHERE course_active = TRUE

-- 2) Which courses were included in the program, but are no longer active?
SELECT course_id AS course_mnemonic, course_name
FROM courses
WHERE course_active = FALSE

-- 3) Which instructors are not current employees?
SELECT instructor_name
FROM instructors
WHERE instructor_active = FALSE
ORDER BY instructor_name;

-- 4) For each course (active and inactive), how many learning outcomes are there?
SELECT c.course_id, c.course_name, COUNT(lo.outcome_id) AS outcome_count
FROM courses c
LEFT JOIN learning_outcomes lo ON c.course_id = lo.course_id
GROUP BY c.course_id, c.course_name
ORDER BY c.course_id;

-- 5) Are there any courses with no learning outcomes?
SELECT c.course_id AS course_mnemonic, c.course_name
FROM courses c
LEFT JOIN learning_outcomes lo ON c.course_id = lo.course_id
WHERE lo.outcome_id IS NULL
ORDER BY c.course_id;

-- 6) Which courses include SQL as a learning outcome?
SELECT DISTINCT c.course_id AS course_mnemonic, c.course_name, lo.outcome_description
FROM courses c
JOIN learning_outcomes lo ON c.course_id = lo.course_id
WHERE LOWER(lo.outcome_description) LIKE '%sql%'
ORDER BY c.course_id;

-- 7) Who taught course ds5100 in Summer 2021?
SELECT i.instructor_name
FROM course_offerings co
JOIN instructors i ON co.instructor_id = i.instructor_id
WHERE co.course_id = 'ds5100' AND co.term_id = 'summer2021';

-- 8) Which instructors taught in Fall 2021?
SELECT DISTINCT i.instructor_name
FROM course_offerings co
JOIN instructors i ON co.instructor_id = i.instructor_id
JOIN terms t ON co.term_id = t.term_id
WHERE t.term_id = 'fall2021'
ORDER BY i.instructor_name;

-- 9) How many courses did each instructor teach in each term?
SELECT t.term_id, i.instructor_name, COUNT(DISTINCT co.course_id) AS course_count
FROM course_offerings co
JOIN instructors i ON co.instructor_id = i.instructor_id
JOIN terms t ON co.term_id = t.term_id
GROUP BY t.term_id, i.instructor_name
ORDER BY t.term_id, i.instructor_name;

-- 10a) Which courses had more than one instructor for the same term?
WITH course_instructor_count AS (
    SELECT term_id, course_id, COUNT(DISTINCT instructor_id) AS instructor_count
    FROM course_offerings
    GROUP BY term_id, course_id
    HAVING COUNT(DISTINCT instructor_id) > 1
)
SELECT c.course_id AS course_mnemonic, t.term_id
FROM course_instructor_count cic
JOIN courses c ON cic.course_id = c.course_id
JOIN terms t ON cic.term_id = t.term_id
ORDER BY t.term_id, c.course_id;

-- 10b) For courses with multiple sections, provide the term, course mnemonic, and instructor name for each.
WITH multi_section_courses AS (
    SELECT term_id, course_id
    FROM course_offerings
    GROUP BY term_id, course_id
    HAVING COUNT(DISTINCT instructor_id) > 1
)
SELECT t.term_id, c.course_id AS course_mnemonic, i.instructor_name
FROM multi_section_courses msc
JOIN course_offerings co ON msc.term_id = co.term_id AND msc.course_id = co.course_id
JOIN courses c ON co.course_id = c.course_id
JOIN instructors i ON co.instructor_id = i.instructor_id
JOIN terms t ON co.term_id = t.term_id
ORDER BY t.term_id, c.course_id, i.instructor_name;
