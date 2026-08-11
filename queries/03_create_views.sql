DROP VIEW IF EXISTS student_report;

CREATE VIEW student_report AS

SELECT

    s.Student_ID,

    e.Attendance,

    e.Assignment_Score,

    e.Study_Hours,

    p.Internal_Test_1,

    p.Internal_Test_2,

    p.Final_Exam_Marks

FROM students s

JOIN performance p
ON s.Student_ID = p.Student_ID

JOIN engagement e
ON s.Student_ID = e.Student_ID;