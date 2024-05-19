import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Magic Conch Game")

# Colors
sky_blue = (255, 225, 235)
black = (0, 0, 0)

# Load images
frog_img = pygame.image.load('frog.jpeg')
frog_img = pygame.transform.scale(frog_img, (50, 50))
tree_img = pygame.image.load('tree.jpeg')
tree_img = pygame.transform.scale(tree_img, (100, 100))

# Define character database and questions
characters = {
    "Noruto": {"anime": True, "male": True, "powers": True, "student": True, "animal_related": False, "image": 'naruto.jpeg'},
    "Mike Mouse": {"anime": False, "male": True, "powers": False, "student": False, "animal_related": True, "image": 'mickey.jpeg'},
    "Sales Moon": {"anime": True, "female": True, "powers": True, "student": True, "animal_related": False, "image": 'sailor_moon.jpeg'},
    "Garfield": {"anime": False, "male": True, "powers": False, "student": False, "animal_related": True, "image": 'garfield.jpeg'},
    "Daughtor Goku": {"anime": True, "male": True, "powers": True, "student": False, "animal_related": False, "image": 'goku.jpeg'}
}

questions = [
    ("Do I look like I'm from an anime?", "anime"),
    ("Am I a male?", "male"),
    ("Do I have superpowers?", "powers"),
    ("Am I a student?", "student"),
    ("Am I related to an animal?", "animal_related")
]
# Function to draw buttons on the screen
def draw_button(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect  # Return the button's rect

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Main game loop
def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    frog_x, frog_y = 200, screen_height // 2
    tree_x = screen_width - 200
    tree_y = screen_height // 2 - 50
    characteristics = {}
    current_question = 0
    frog_moving = True
    game_over = False
    yes_button = None
    no_button = None
    user_input = None
    while current_question < len(questions) and not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not frog_moving:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button and yes_button.collidepoint(mouse_pos):
                    characteristics[questions[current_question][1]] = True
                    user_input = 'Yes'
                    current_question += 1
                    frog_moving = True
                elif no_button and no_button.collidepoint(mouse_pos):
                    characteristics[questions[current_question][1]] = False
                    user_input = 'No'
                    current_question += 1
                    frog_moving = True

        screen.fill(sky_blue)

        # Draw the frog
        screen.blit(frog_img, (frog_x, frog_y))

        # Draw the tree
        screen.blit(tree_img, (tree_x, tree_y))

        # Display the question only when the frog is not moving
        if not frog_moving and current_question < len(questions):
            draw_text(questions[current_question][0], font, black, screen, 20, 20)
            yes_button = draw_button('Yes (y)', font, black, screen, screen_width // 2 - 50, screen_height - 50)
            no_button = draw_button('No (n)', font, black, screen, screen_width // 2 + 50, screen_height - 50)
            if user_input is not None:
                draw_text(f'You answered: {user_input}', font, black, screen, 20, 60)

        # Move the frog towards the tree
        if frog_moving:
            frog_x += 5
            if frog_x + frog_img.get_width() >= tree_x:
                frog_moving = False

        pygame.display.flip()
        clock.tick(30)

    # Determine the character based on the answers
    result = find_character(characteristics)

    # Display the result
    if result:
        character_img = pygame.image.load(characters[result]['image'])
        character_img = pygame.transform.scale(character_img, (300, 300))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(sky_blue)
            # If the guess is correct, make the frog jump up and down
            if result:
                frog_y -= 5
                if frog_y <= screen_height // 2 - 100:
                    frog_y += 5  # Move frog back down
                    draw_text("Hooray! I got it right!", font, black, screen, 20, 20)
                    draw_text(f"I am {result}!", font, black, screen, 20, 60)
                    screen.blit(character_img, (screen_width // 2, screen_height // 2))
                    pygame.display.flip()
                    time.sleep(10)  # Wait for 10 seconds
                    pygame.quit()
                    sys.exit()
            else:
                # If the guess is wrong, make the frog fall down
                frog_y += 5
                if frog_y >= screen_height:
                    draw_text("Oh no! I fell off the tree!", font, black, screen, 20, 20)
                    pygame.display.flip()
                    time.sleep(10)  # Wait for 10 seconds
                    pygame.quit()
                    sys.exit()

            screen.blit(frog_img, (frog_x, frog_y))
            pygame.display.flip()
            clock.tick(30)

    else:
        # If all answers are incorrect, display a message and wait for 10 seconds
        draw_text("Oops! I couldn't guess the character.", font, black, screen, 20, 20)
        pygame.display.flip()
        time.sleep(10)  # Wait for 10 seconds
        pygame.quit()
        sys.exit()


# Function to find the character based on the characteristics
def find_character(characteristics):
    for name, attrs in characters.items():
        match = all(attrs.get(k) == v for k, v in characteristics.items())
        if match:
            return name
    return None


if __name__ == "__main__":
    main()
