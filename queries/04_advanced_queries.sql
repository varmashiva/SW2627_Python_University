-- =====================================================
-- JOIN
-- =====================================================

SELECT
    s.Student_ID,
    p.Final_Exam_Marks,
    e.Attendance
FROM students s
JOIN performance p
ON s.Student_ID = p.Student_ID
JOIN engagement e
ON s.Student_ID = e.Student_ID
LIMIT 10;


-- =====================================================
-- GROUP BY
-- =====================================================

SELECT

CASE

WHEN Attendance >= 90 THEN 'Excellent'

WHEN Attendance >= 75 THEN 'Good'

WHEN Attendance >= 60 THEN 'Average'

ELSE 'Poor'

END AS Attendance_Category,

ROUND(AVG(Final_Exam_Marks),2) AS Average_Final_Marks

FROM student_report

GROUP BY Attendance_Category;


-- =====================================================
-- HAVING
-- =====================================================

SELECT

CASE

WHEN Attendance >= 90 THEN 'Excellent'

WHEN Attendance >= 75 THEN 'Good'

WHEN Attendance >= 60 THEN 'Average'

ELSE 'Poor'

END AS Attendance_Category,

ROUND(AVG(Final_Exam_Marks),2) AS Average_Final_Marks

FROM student_report

GROUP BY Attendance_Category

HAVING Average_Final_Marks > 70;


-- =====================================================
-- SUBQUERY
-- =====================================================

SELECT *

FROM student_report

WHERE Final_Exam_Marks >

(
SELECT AVG(Final_Exam_Marks)

FROM student_report
);


-- =====================================================
-- ORDER BY
-- =====================================================

SELECT *

FROM student_report

ORDER BY Final_Exam_Marks DESC

LIMIT 10;


-- =====================================================
-- CASE + GROUP BY
-- =====================================================

SELECT

CASE

WHEN Final_Exam_Marks >= 90 THEN 'A'

WHEN Final_Exam_Marks >= 80 THEN 'B'

WHEN Final_Exam_Marks >= 70 THEN 'C'

WHEN Final_Exam_Marks >= 60 THEN 'D'

WHEN Final_Exam_Marks >= 50 THEN 'E'

ELSE 'F'

END AS Grade,

COUNT(*) AS Total_Students

FROM student_report

GROUP BY Grade;