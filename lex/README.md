# Lex
This session details the structure of the bot itself; while simple, it contains important information with regard to utterance/intent/response structure.

## Intents/Slots
- **GetStep:** This intent will navigate to a specified step in the lesson. This does not handle sequential maneuver through the lessons, but directed navigation to a step specified by the user. 
    - **'step' Slot:** This slot will store the number of the step that the student would like to navigate to. This is utilized inside of Lambda to load the appropriate step content.
- **Greeting:** A simple intent designed to provide some level of dynamic between the bot and user.
    - **'name' Slot:** Stores the name the user provides to the bot.
- **NextStep:** This intent is triggered by the user's request to move to the next step in the lesson sequentially. The work of this intent is performed in Lambda rather than Lex.
- **PrevStep:** This intent is triggered by the user's request to move to the next step in the lesson sequentially. The work of this intent is performed in Lambda rather than Lex.
- **Tutorials:** This intent handles the interaction with the user eliciting the specific lesson they would like to do. Depending on what data the user provides, it will ask further questions or provide the user with the selection options.
    - **'Lessons' Slot:** This slot holds the specific name of the lesson or category the user would like to view, or the "search" that the user would like to make into the lessons.

## Error Handling
Error handling is heavily controlled/managed in Lambda, but in the cases where Lex cannot determine the intent from the utterance, it will return a simple error message. 

## Expansion/Improvement
A few ways the current iteration can be improved are as follows:
- Dynamic intent approximation from a database rather than "hard-coded"
- More dynamic "conversation" with the user to make it more "human"