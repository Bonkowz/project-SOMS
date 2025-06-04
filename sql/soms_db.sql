DROP DATABASE IF EXISTS soms;
CREATE DATABASE soms;
USE soms;

-- Users table for login
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Insert a sample user
INSERT INTO users (username, password) VALUES ('gift', 'useruser');


-- Member table
CREATE TABLE member (
    student_id INT(9) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    enrollment_status VARCHAR(15) NOT NULL,
    email_address VARCHAR(50) UNIQUE,
    member_name VARCHAR(50) NOT NULL,
    batch_year_of_enrollment INT(4) NOT NULL,
    degree_program VARCHAR(50) NOT NULL,
    member_total_unpaid_fees DECIMAL(10, 4),
    graduation_date DATE,
    PRIMARY KEY (student_id)
);

-- Organization table
CREATE TABLE organization (
    organization_id INT(9) NOT NULL,
    no_of_members INT(3),
    organization_name VARCHAR(50) NOT NULL,
    organization_type VARCHAR(50),
    total_paid_fees DECIMAL(10, 4),
    total_unpaid_fees DECIMAL(10, 4),
    PRIMARY KEY (organization_id)
);

-- Fee table
CREATE TABLE fee (
    fee_id INT(9) NOT NULL,
    amount DECIMAL(10, 4),
    payment_status VARCHAR(15) NOT NULL,
    due_date DATE NOT NULL,
    pay_date DATE,
    school_year INT(4),
    semester VARCHAR(10),
    organization_id INT(9),
    student_id INT(9),
    PRIMARY KEY (fee_id),
    FOREIGN KEY (organization_id) REFERENCES organization(organization_id),
    FOREIGN KEY (student_id) REFERENCES member(student_id) ON DELETE CASCADE
);

-- Member Serves table
CREATE TABLE member_serves (
    school_year INT(4),
    membership_status VARCHAR(15) NOT NULL,
    batch_year_of_membership INT(4),
    semester VARCHAR(10),
    committee_role VARCHAR(50),
    committee VARCHAR(50),
    organization_id INT(9),
    student_id INT(9),
    PRIMARY KEY (organization_id, student_id, school_year),
    FOREIGN KEY (organization_id) REFERENCES organization(organization_id),
    FOREIGN KEY (student_id) REFERENCES member(student_id) ON DELETE CASCADE
);

INSERT INTO organization VALUES
(101, 17, 'UP Oroquieta', 'Varsitarian', 1000.00, 500.00),
(102, 17, 'UP Silakbo', 'Music', 500.00, 100.00),
(104, 0, 'Aiesec', 'Cultural', 500.0, 100.0),
(105, 0, 'Alyansa Ng Mga Kabitenyo Sa Uplb', 'Cultural', 510.25, 108.75),
(106, 0, 'Ana Kalang Society', 'Cultural', 520.5, 117.5),
(107, 0, 'Anakbayan Up Los Baños', 'Cultural', 530.75, 126.25),
(108, 0, 'Astronomical Society', 'Cultural', 541.0, 135.0),
(109, 0, 'Ahon Batang Calabarzon - Uplb', 'Cultural', 551.25, 143.75),
(110, 0, 'Alleluia Community-christ`s Youth In Action Uplb', 'Cultural', 561.5, 152.5),
(111, 0, 'Alliance Of Gamers', 'Cultural', 571.75, 161.25),
(112, 0, 'Banahaw', 'Cultural', 582.0, 170.0),
(113, 0, 'Basketboleros, Basketboleras: Ang Ligang Lamang', 'Cultural', 592.25, 178.75);

INSERT INTO member VALUES
(2023001, 'Male', 'Enrolled', 'john@mail.com', 'John Doe', 2023, 'BSCS', 100.00, NULL),
(2023002, 'Female', 'Enrolled', 'jane@mail.com', 'Jane Smith', 2023, 'BSN', 0.00, NULL),
(2023003, 'Male', 'Graduated', 'mike@mail.com', 'Mike Johnson', 2021, 'BSCS', 50.00, '2025-06-01'),
(2023004, 'Male', 'Graduated', 'alex2023004@mail.com', 'Alex Kim', 2022, 'BS Math', 125.77, '2026-03-13'),
(2023005, 'Male', 'Enrolled', 'morgan2023005@mail.com', 'Morgan Smith', 2022, 'BS Math', 94.79, NULL),
(2023006, 'Female', 'Enrolled', 'morgan2023006@mail.com', 'Morgan Smith', 2022, 'BSN', 169.80, NULL),
(2023007, 'Male', 'Graduated', 'jordan2023007@mail.com', 'Jordan Lee', 2021, 'BS Math', 99.65, '2025-09-22'),
(2023008, 'Female', 'Graduated', 'casey2023008@mail.com', 'Casey Garcia', 2021, 'BSN', 160.59, '2025-06-14'),
(2023009, 'Male', 'Enrolled', 'taylor2023009@mail.com', 'Taylor Patel', 2022, 'BSN', 57.81, NULL),
(2023010, 'Female', 'Enrolled', 'sam2023010@mail.com', 'Sam Lee', 2022, 'BA Comm', 104.00, NULL),
(2023011, 'Female', 'Graduated', 'jordan2023011@mail.com', 'Jordan Rodriguez', 2021, 'BSN', 121.59, '2025-11-05'),
(2023012, 'Female', 'Enrolled', 'drew2023012@mail.com', 'Drew Rodriguez', 2023, 'BS Math', 86.31, NULL),
(2023013, 'Female', 'Enrolled', 'taylor2023013@mail.com', 'Taylor Nguyen', 2022, 'BS Math', 31.15, NULL);

INSERT INTO member VALUES
(2023014, 'Male', 'Enrolled', 'member14@mail.com', 'Student Fourteen', 2023, 'BSCS', 0.00, NULL),
(2023015, 'Female', 'Enrolled', 'member15@mail.com', 'Student Fifteen', 2022, 'BSN', 0.00, NULL),
(2023016, 'Male', 'Enrolled', 'member16@mail.com', 'Student Sixteen', 2023, 'BS Math', 0.00, NULL),
(2023017, 'Female', 'Graduated', 'member17@mail.com', 'Student Seventeen', 2021, 'BA Comm', 0.00, '2025-01-01'),
(2023018, 'Male', 'Enrolled', 'member18@mail.com', 'Student Eighteen', 2022, 'BSCS', 0.00, NULL),
(2023019, 'Female', 'Enrolled', 'member19@mail.com', 'Student Nineteen', 2023, 'BSN', 0.00, NULL),
(2023020, 'Male', 'Graduated', 'member20@mail.com', 'Student Twenty', 2021, 'BS Math', 0.00, '2025-01-01'),
(2023021, 'Female', 'Enrolled', 'member21@mail.com', 'Student TwentyOne', 2022, 'BA Comm', 0.00, NULL),
(2023022, 'Male', 'Enrolled', 'member22@mail.com', 'Student TwentyTwo', 2023, 'BSCS', 0.00, NULL),
(2023023, 'Female', 'Enrolled', 'member23@mail.com', 'Student TwentyThree', 2021, 'BSN', 0.00, NULL),

(2024001, 'Male', 'Enrolled', 'member24001@mail.com', 'New Student One', 2024, 'BSCS', 0.00, NULL),
(2024002, 'Female', 'Enrolled', 'member24002@mail.com', 'New Student Two', 2023, 'BSN', 0.00, NULL),
(2024003, 'Male', 'Enrolled', 'member24003@mail.com', 'New Student Three', 2024, 'BS Math', 0.00, NULL),
(2024004, 'Female', 'Graduated', 'member24004@mail.com', 'New Student Four', 2022, 'BA Comm', 0.00, '2026-06-01'),
(2024005, 'Male', 'Enrolled', 'member24005@mail.com', 'New Student Five', 2023, 'BSCS', 0.00, NULL),
(2024006, 'Female', 'Enrolled', 'member24006@mail.com', 'New Student Six', 2024, 'BSN', 0.00, NULL),
(2024007, 'Male', 'Graduated', 'member24007@mail.com', 'New Student Seven', 2022, 'BS Math', 0.00, '2026-06-01'),
(2024008, 'Female', 'Enrolled', 'member24008@mail.com', 'New Student Eight', 2023, 'BA Comm', 0.00, NULL),
(2024009, 'Male', 'Enrolled', 'member24009@mail.com', 'New Student Nine', 2024, 'BSCS', 0.00, NULL),
(2024010, 'Female', 'Enrolled', 'member24010@mail.com', 'New Student Ten', 2022, 'BSN', 0.00, NULL),
(2024011, 'Male', 'Enrolled', 'member24011@mail.com', 'New Student Eleven', 2024, 'BS Math', 0.00, NULL),
(2024012, 'Female', 'Enrolled', 'member24012@mail.com', 'New Student Twelve', 2023, 'BA Comm', 0.00, NULL),
(2024013, 'Male', 'Enrolled', 'member24013@mail.com', 'New Student Thirteen', 2023, 'BSCS', 0.00, NULL),
(2024014, 'Female', 'Enrolled', 'member24014@mail.com', 'New Student Fourteen', 2024, 'BSN', 0.00, NULL),

(2025001, 'Male', 'Enrolled', 'member25001@mail.com', 'Student 25001', 2025, 'BSCS', 0.00, NULL),
(2025002, 'Female', 'Enrolled', 'member25002@mail.com', 'Student 25002', 2024, 'BSN', 0.00, NULL),
(2025003, 'Male', 'Enrolled', 'member25003@mail.com', 'Student 25003', 2025, 'BS Math', 0.00, NULL),
(2025004, 'Female', 'Enrolled', 'member25004@mail.com', 'Student 25004', 2024, 'BA Comm', 0.00, NULL),
(2025005, 'Male', 'Enrolled', 'member25005@mail.com', 'Student 25005', 2023, 'BSCS', 0.00, NULL),
(2025006, 'Female', 'Enrolled', 'member25006@mail.com', 'Student 25006', 2025, 'BSN', 0.00, NULL),
(2025007, 'Male', 'Enrolled', 'member25007@mail.com', 'Student 25007', 2024, 'BS Math', 0.00, NULL),
(2025008, 'Female', 'Enrolled', 'member25008@mail.com', 'Student 25008', 2025, 'BA Comm', 0.00, NULL),
(2025009, 'Male', 'Enrolled', 'member25009@mail.com', 'Student 25009', 2024, 'BSCS', 0.00, NULL),
(2025010, 'Female', 'Enrolled', 'member25010@mail.com', 'Student 25010', 2023, 'BSN', 0.00, NULL);


INSERT INTO member_serves VALUES
(2023, 'Active', 2023, '1', 'President', '', 101, 2023014),
(2023, 'Active', 2022, '1', 'President', '', 102, 2023015),
(2023, 'Active', 2023, '1', 'VP', 'Membership', 101, 2023016),
(2023, 'Alumni', 2021, '1', 'Member', 'Publicity', 102, 2023017),
(2023, 'Active', 2022, '1', 'Treasurer', 'Finance', 101, 2023018),
(2023, 'Inactive', 2023, '2', 'Member', 'Logistics', 102, 2023019),
(2023, 'Alumni', 2021, '1', 'Secretary', 'Finance', 101, 2023020),
(2023, 'Active', 2022, '1', 'Member', 'Membership', 102, 2023021),
(2023, 'Inactive', 2023, '1', 'VP', 'Publicity', 101, 2023022),
(2023, 'Active', 2021, '1', 'Member', 'Finance', 102, 2023023),
(2024, 'Active', 2024, '1', 'Member', 'Events', 101, 2024001),
(2024, 'Inactive', 2023, '1', 'Member', 'Publicity', 102, 2024002),
(2024, 'Active', 2024, '1', 'Secretary', 'Logistics', 101, 2024003),
(2024, 'Alumni', 2022, '1', 'Member', 'Finance', 102, 2024004),
(2024, 'Active', 2023, '1', 'VP', 'Events', 101, 2024005),
(2024, 'Inactive', 2024, '2', 'Member', 'Membership', 102, 2024006),
(2024, 'Alumni', 2022, '1', 'Treasurer', 'Finance', 101, 2024007),
(2024, 'Active', 2023, '1', 'Member', 'Logistics', 102, 2024008),
(2024, 'Inactive', 2024, '1', 'VP', 'Publicity', 101, 2024009),
(2024, 'Active', 2022, '1', 'Member', 'Membership', 102, 2024010),
(2024, 'Active', 2024, '2', 'Member', 'Outreach', 101, 2024011),
(2024, 'Inactive', 2023, '2', 'VP', 'Logistics', 102, 2024012),
(2024, 'Active', 2023, '1', 'President', '', 101, 2024013),
(2024, 'Active', 2024, '1', 'President', '', 102, 2024014),
(2025, 'Active', 2025, '1', 'President', '', 101, 2025001),
(2025, 'Active', 2024, '1', 'VP', 'Logistics', 102, 2025002),
(2025, 'Active', 2025, '1', 'Member', 'Events', 101, 2025003),
(2025, 'Inactive', 2024, '2', 'Member', 'Publicity', 102, 2025004),
(2025, 'Alumni', 2023, '1', 'Secretary', 'Finance', 101, 2025005),
(2025, 'Active', 2025, '1', 'President', '', 102, 2025006),
(2025, 'Active', 2024, '2', 'Member', 'Membership', 101, 2025007),
(2025, 'Inactive', 2025, '1', 'Treasurer', 'Audit', 102, 2025008),
(2025, 'Active', 2024, '1', 'Member', 'Outreach', 101, 2025009),
(2025, 'Alumni', 2023, '2', 'VP', 'Events', 102, 2025010);

INSERT INTO fee VALUES
(1, 100.00, 'Paid', '2024-03-01', '2024-02-28', 2024, '1', 101, 2023001),
(2, 50.00, 'Not Paid', '2024-04-01', NULL, 2024, '1', 101, 2023002),
(3, 100.00, 'Paid', '2024-03-15', '2024-03-20', 2024, '1', 102, 2023003),
(4, 100.00, 'Paid', '2024-04-28', '2024-05-29', 2024, '1', 101, 2023013),
(5, 75.00, 'Not Paid', '2024-04-25', NULL, 2024, '1', 102, 2023009),
(6, 50.00, 'Paid', '2024-04-26', '2024-04-26', 2024, '2', 101, 2023012),
(7, 75.00, 'Not Paid', '2024-04-01', NULL, 2024, '1', 101, 2023009),
(8, 50.00, 'Not Paid', '2024-05-12', NULL, 2024, '2', 102, 2023009),
(9, 100.00, 'Paid', '2024-04-04', '2024-05-21', 2024, '1', 102, 2023011),
(10, 75.00, 'Paid', '2024-05-13', '2024-04-20', 2024, '2', 101, 2023011),
(11, 100.00, 'Not Paid', '2024-05-06', NULL, 2024, '1', 101, 2023011),
(12, 50.00, 'Paid', '2024-04-08', '2024-04-15', 2024, '1', 101, 2023013),
(13, 50.00, 'Paid', '2024-04-02', '2024-04-16', 2024, '2', 102, 2023010);