-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: sophia
-- Generation Time: Nov 18, 2023 at 02:41 PM
-- Server version: 5.7.42-0ubuntu0.18.04.1
-- PHP Version: 8.2.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `zyzhong2`
--

-- --------------------------------------------------------

--
-- Table structure for table `class_session`
--

CREATE TABLE `class_session` (
  `course_id` int(11) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `class_addr` text CHARACTER SET utf8 NOT NULL,
  `date` varchar(10) CHARACTER SET utf8 NOT NULL,
  `zoom_link` text CHARACTER SET utf8 NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `class_session` (`course_id`, `start_time`, `end_time`, `class_addr`, `date`, `zoom_link`) VALUES
(1, '16:30:00', '18:00:00', 'CBA', 'MON', "https://hku.zoom.us/j/3425071876"),
(2, '09:30:00', '11:00:00', 'CYPP2', 'THU', "https://hku.zoom.us/j/3425071876"),
(3, '11:30:00', '13:00:00', 'CYPP2', 'FRI', "https://hku.zoom.us/j/3425071876"),
(4, '14:00:00', '15:30:00', 'EH101', 'WED', "https://hku.zoom.us/j/3425071876"),
(5, '15:30:00', '17:00:00', 'JLG01', 'FRI', NULL),
(6, '16:30:00', '18:00:00', 'KB132', 'TUE', "https://hku.zoom.us/j/3425071876"),
(7, '11:00:00', '12:30:00', 'KK101', 'MON', NULL),
(8, '13:30:00', '15:00:00', 'CYCP1', 'FRI', NULL),
(9, '15:30:00', '17:00:00', 'CYPP2', 'THU', NULL),
(10, '09:30:00', '11:00:00', 'CYPP3', 'WED', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `course_id` int(11) NOT NULL,
  `course_code` varchar(80) CHARACTER SET utf8 NOT NULL,
  `course_name` varchar(80) CHARACTER SET utf8 NOT NULL,
  `instructor_name` varchar(80) CHARACTER SET utf8 NOT NULL,
  `teacher_msg` varchar(200) CHARACTER SET utf8 NOT NULL,
  `course_info` varchar(200) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `course` (`course_id`, `course_code`, `course_name`, `instructor_name`, `teacher_msg`, `course_info`) VALUES
(1, 'COMP3323', 'Advanced Database Systems', 'Cheng Reynold', "Welcome to Advanced Database Systems!", "Able to understand the background and knowledge of some advanced topics in database that have become key techniques in modern database theory and practices; typical topics are distributed concurrency control, database recovery, query optimization, spatial databases."),
(2, 'COMP3329', 'Computer Game Design and Programming', 'Chim T W', "Get ready to create amazing games!", "Be able to implement a workable game in particular platform; Be able to understand different aspects of game design including UI, programming, marketing, etc; Be able to present the game idea in both written and oral form."),
(3, 'COMP3330', 'Interactive Mobile Application Design and Programming', 'Chim T W', "Let's build some awesome mobile apps!", "Understand the basics about mobile computing, including the devices, applications, markets, and eco-systems"),
(4, 'COMP3340', 'Applied Deep Learning', 'Luo Ping', "Dive into the world of deep learning with us!", "understand the motivations and principles for building deep learning systems based on empirical data, and how deep learning relates to the broader field of artificial intelligence."),
(5, 'COMP3351', 'Advanced Algorithm Analysis', 'Huang Z.Y.', "Learn the secrets of efficient algorithms!", "Understand abstract mathematical concepts which are involved in designing advanced algorithms, e.g., probability theory, conditional expectation, Markov's inequality, measure concentration."),
(6, 'COMP3353', 'Bioinformatics', 'Luo Ruibang', "Explore the intersection of biology and computer science!", "Be able to understand the important algorithms used in bioinformatics; Be able to understand the theoretical foundations and applications for several leading bioinformatics tools."),
(7, 'COMP3355', 'Cyber Security', 'Qian Chenxiong', "Stay one step ahead of cyber threats!", "Be able to understand the principles and objectives of information security, encryption, cyber-attacks and defense; Be able to understand security models and to apply the model to achieve the security objectives."),
(8, 'COMP3356', 'Robotics', 'Pan Jia', "Join us in building the robots of the future!", "Understand the motivations and principles for building autonomous robotic system based on sensory perception, control principles, and AI algorithms; and how robotics relates to the broader field of artificial intelligence"),
(9, 'COMP3357', 'Cryptography', 'Ramanathan Ravishankar', "Unlock the mysteries of secure communication!", " Understand the basic elementary knowledge of one-way function, such as discrete logarithm and RSA. Learn the elementary tools of pseudorandom number generator. Be familiar with tools of quantum information theory. Understand the basics of modern quantum cryptography including quantum key distribution and quantum random number generation."),
(10, 'COMP3358', 'Distributed and Parallel Computing', 'Cui H.M.', "Master the art of high-performance computing!", " Students are able to apply distributed and parallel computing concepts, to make correct conceptual choices, and to design software architectures for solving real-world problems.");

-- --------------------------------------------------------

--
-- Table structure for table `courseMaterial`
--

CREATE TABLE `courseMaterial` (
  `course_id` int(11) NOT NULL,
  `material_name` varchar(80) CHARACTER SET utf8 NOT NULL,
  `link` text CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `courseMaterial` (`course_id`, `material_name`, `link`) VALUES
(1, 'Advanced Database Systems', 'https://books.google.com.hk'),
(2, 'Computer game design: Opportunities for successful learning', 'https://www.sciencedirect.com/science/article/abs/pii/S0360131507001078'),
(2, 'How to Become a Game Designer', 'https://www.youtube.com/watch?v=PMXf0e8n2Oc&t=817s'),
(3, 'COMP3330 course syllabus', 'https://www.cs.hku.hk/index.php/programmes/course-offered?infile=2019/comp3330.html'),
(4, 'Applied Deep Learning', 'https://link.springer.com/book/10.1007/978-1-4842-3790-8'),
(5, 'No material yet', ''),
(6, 'A brief history of bioinformatics', 'https://academic.oup.com/bib/article/20/6/1981/5066445'),
(7, 'What is Cyber Security?', 'https://www.kaspersky.com/resource-center/definitions/what-is-cyber-security'),
(8, 'The evolution of robotics research', 'https://ieeexplore.ieee.org/abstract/document/4141037'),
(8, 'Introduction to AI Robotics, second edition', 'https://books.google.com.hk'),
(9, 'No material yet', ''),
(10, 'No material yet', ''),
(1, 'Lecture1', 'https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/resources/lecture16webhan/'),
(3, 'Lecture1', 'https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/resources/lecture16webhan/'),
(5, 'Lecture1', 'https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/resources/lecture16webhan/'),
(7, 'Lecture1', 'https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/resources/lecture16webhan/'),
(9, 'Lecture1', 'https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/resources/lecture16webhan/'),
(2, 'Lecture1', 'https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/resources/lecture16webhan/'),
(2, 'Lecture2', 'https://drive.google.com/file/d/1RYkJiGb2ytUDirW5dRDbrjcscitGHuae/view?usp=sharing'),
(2, 'Lecture3', 'https://drive.google.com/file/d/1uB_4_wgLqR-0DLkzAfrmYjFQKGklycFd/view?usp=sharing'),
(4, 'Lecture1', 'https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/resources/lecture16webhan/'),
(6, 'Lecture1', 'https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/resources/lecture16webhan/'),
(8, 'Lecture1', 'https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/resources/lecture16webhan/'),
(10, 'Lecture1', 'https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/resources/lecture16webhan/');

-- --------------------------------------------------------

--
-- Table structure for table `enrolls_in`
--

CREATE TABLE `enrolls_in` (
  `course_id` int(11) NOT NULL,
  `uid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `enrolls_in` (`course_id`, `uid`) VALUES
(1, 30350001),
(2, 30350001),
(4, 30350001),
(5, 30350001),
(7, 30350001),

(2, 30350002),
(3, 30350002),
(4, 30350002),
(6, 30350002),
(8, 30350002),

(1, 30350003),
(3, 30350003),
(4, 30350003),
(5, 30350003),
(9, 30350003),

(2, 30350004),
(3, 30350004),
(4, 30350004),
(6, 30350004),
(7, 30350004),

(1, 30350005),
(2, 30350005),
(3, 30350005),
(4, 30350005),
(8, 30350005),

(2, 30350006),
(4, 30350006),
(5, 30350006),
(6, 30350006),
(10, 30350006),

(1, 30350007),
(3, 30350007),
(5, 30350007),
(6, 30350007),
(8, 30350007),

(1, 30350008),
(2, 30350008),
(3, 30350008),
(4, 30350008),
(9, 30350008),

(1, 30350009),
(2, 30350009),
(5, 30350009),
(6, 30350009),
(10, 30350009),

(3, 30350010),
(4, 30350010),
(5, 30350010),
(7, 30350010),
(8, 30350010);

--
-- Dumping data for table `enrolls_in`
--

-- --------------------------------------------------------

--
-- Table structure for table `login_records`
--

CREATE TABLE `login_records` (
  `uid` int(11) NOT NULL,
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_time` datetime NOT NULL,
  `logout_time` datetime NOT NULL,
  `duration` float NOT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `login_records` (`uid`, `login_time`, `logout_time`, `duration`) VALUES
(30350001, '2023-11-15 09:00:00', '2023-11-15 10:30:00', 90),
(30350001, '2023-11-16 14:00:00', '2023-11-16 15:30:00', 90),
(30350002, '2023-11-14 11:00:00', '2023-11-14 12:30:00', 90),
(30350002, '2023-11-16 16:00:00', '2023-11-16 18:00:00', 120),
(30350003, '2023-11-15 09:00:00', '2023-11-15 11:00:00', 120),
(30350003, '2023-11-16 14:00:00', '2023-11-16 15:00:00', 60),
(30350003, '2023-11-17 11:00:00', '2023-11-17 12:00:00', 60),
(30350004, '2023-11-15 14:00:00', '2023-11-15 15:30:00', 90),
(30350004, '2023-11-16 10:00:00', '2023-11-16 11:30:00', 90),
(30350004, '2023-11-17 14:00:00', '2023-11-17 16:00:00', 120),
(30350005, '2023-11-14 09:00:00', '2023-11-14 11:00:00', 120),
(30350005, '2023-11-15 16:00:00', '2023-11-15 17:30:00', 90),
(30350005, '2023-11-16 11:00:00', '2023-11-16 12:30:00', 90);

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `uid` int(10) NOT NULL,
  `name` varchar(80) CHARACTER SET utf8 NOT NULL,
  `email` varchar(80) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `student` (`uid`, `name`, `email`) VALUES
(30350001, 'Alex', 'Hzy1372506813@hotmail,com'),
(30350002, 'Bob', 'hzyalex217@gmail.com'),
(30350003, 'Cindy', 'hzyalex@connect.hku.hk');
-- --------------------------------------------------------

--
-- Table structure for table `studentList`
--

CREATE TABLE `studentList` (
  `uid` int(11) NOT NULL,
  `gpa` float(11) NOT NULL,
  `major` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `studentList`
--

INSERT INTO `studentList` (`uid`, `gpa`, `major`) VALUES
(30350001, 3.21, 'Computer Science'),
(30350002, 3.45, 'Computer Engineering'),
(30350003, 3.67, 'Electrical Engineering'),
(30350004, 3.89, 'Mechanical Engineering'),
(30350005, 3.12, 'Civil Engineering'),
(30350006, 3.34, 'Chemical Engineering'),
(30350007, 3.56, 'Biomedical Engineering'),
(30350008, 3.78, 'Industrial Engineering'),
(30350009, 3.90, 'Environmental Engineering'),
(30350010, 3.23, 'Materials Engineering');



--
-- Indexes for dumped tables
--

--
-- Indexes for table `class_session`
--
ALTER TABLE `class_session`
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`course_id`);

--
-- Indexes for table `courseMaterial`
--
ALTER TABLE `courseMaterial`
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `login_records`
--
ALTER TABLE `login_records`
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`uid`);

--
-- Indexes for table `studentList`
--
ALTER TABLE `studentList`
  ADD KEY `i` (`uid`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `class_session`
--
ALTER TABLE `class_session`
  ADD CONSTRAINT `class_session_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

--
-- Constraints for table `courseMaterial`
--
ALTER TABLE `courseMaterial`
  ADD CONSTRAINT `courseMaterial_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

--
-- Constraints for table `login_records`
--
ALTER TABLE `login_records`
  ADD CONSTRAINT `login_records_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `studentList` (`uid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
