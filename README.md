# BMX IQ Race (version 2.1.1) - Online Gaming Platform

![BMX IQ Race](https://i.ibb.co/XjKBnKg/circle-logo-1.png)

## BMX IQ Race Links

- [Live Site](http://bmxrace.uk.to/)
- [YouTube Demo](https://youtu.be/0RVEKCt_jwU)

BMX IQ Race is an exciting online gaming platform that challenges players' knowledge and skills in various categories, including Mathematics, General Knowledge, and three Olympic-themed categories. Players get to compete in a thrilling BMX race while answering quiz questions, making it a unique and engaging educational experience.

## Features 1.1.0

- Engaging quiz-based gameplay with real-time BMX racing.
- Categories including Mathematics, General Knowledge, and three Olympic-themed categories.
- Seamless and interactive experience powered by WebSockets for real-time communication during gameplay.
- User-friendly interface with an attractive design.
- Developed with Django for robust backend and frontend.

## New Updates 2.0.0

- **Global Chat Feature:** We've added a global chat feature that allows players from all over the world to interact, share tips, and make new friends while enjoying the game.
- **Enhanced UI:** Our UI has undergone significant improvements to provide a more intuitive and visually appealing experience for players. Navigating through the game is now even more enjoyable!

## New Updates 2.1.0

- **Global Chat Feature:** Critical Bug fixing that disallows any other to mask your identity and chat.
- **Global Leaderboard:** The leaderboard has been enhanced with win rate and predicting score. Compete with other players and see how you rank globally!
- **Game Engine:** Major bug fixing that enhances player user experience and score. We have also added more interesting topics to play the quiz with.
- **Account Deletion Option:** We've introduced a new option in settings that allows users to permanently delete their account from the database. Your data, scores, and progress can now be permanently removed if you choose to do so.

## New Updates 2.1.1

- **Secure Post Method Triggering:** We've implemented additional security measures to ensure that the post method triggering is secure and protected against potential attacks or unauthorized access.
- **Account Deletion:** The account deletion feature now requires manual confirmation to prevent accidental account deletion. Users cannot access the account deletion process through direct links, ensuring more intentional account deletion actions.

## Some Edge Cases (hard and sensitive bugs)

- **During Gameplay:** Compilation of the score might clash with each other if a player left and finished at the same time, potentially applying the scoring system for both due to the need for a precise server system to track the sub-ticks, providing every millisecond information.
- **Matchmaking Timer:** Matchmaking time is not perfectly precise, with a delay of 1-2 seconds. When a player leaves at the exact moment another player starts, they may be paired up and matched without the first player.

We are continuously working on further improvements and updates to make BMX IQ Race a more enjoyable and secure gaming platform. Happy gaming and learning! 🚀🚴‍♂️
