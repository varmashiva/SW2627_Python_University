-- Total Students
SELECT COUNT(*) AS Total_Students
FROM student_performance;

-- Average Attendance
SELECT ROUND(AVG(Attendance),2) AS Average_Attendance
FROM student_performance;

-- Top 10 Students
SELECT Student_ID,
       Final_Exam_Marks
FROM student_performance
ORDER BY Final_Exam_Marks DESC
LIMIT 10;

-- Students at Risk
SELECT Student_ID,
       Final_Exam_Marks
FROM student_performance
WHERE Final_Exam_Marks < 50;

-- Average Marks
SELECT ROUND(AVG(Final_Exam_Marks),2)
AS Average_Final_Marks
FROM student_performance;