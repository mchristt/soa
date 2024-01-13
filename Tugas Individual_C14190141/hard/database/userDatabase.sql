SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `users` (
  `id` longtext NOT NULL,
  `userNRP` longtext NOT NULL,
  `userName` longtext NOT NULL,
  `userEmail` longtext NOT NULL,
  `userPassword` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO `users` (`id`, `userNRP`, `userName`,`userEmail`,`userPassword`) VALUES
('b5fd2696-9afc-4d16-bb2a-f44283104fe7','c14190141', 'Christ', 'c14190141@john.petra.ac.id','kurisu14'),
('7af56368-09a1-47cf-a96e-876e5780bcfa', 'c14180098','test1','c14180098@john.petra.ac.id', 'testotesto'),
('3a57fc0c-a845-4cc5-b5a2-eb04fcb3786c', 'c14190001','test2','c14190001@john.petra.ac.id', 'testotesto123');
COMMIT;