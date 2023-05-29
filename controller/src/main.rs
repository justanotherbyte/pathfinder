mod platforms;

use device_query::{DeviceEvents, DeviceState, Keycode};

use platforms::{PlatformHandler, RedisMessage, Motor, Direction};

#[tokio::main]
async fn main() {
    let handler = platforms::MessageHandler::new();
    let device_state = DeviceState::new();
    
    let down_handler = handler.clone();
    let up_handler = handler.clone();
    let _guard = device_state.on_key_down(move |key| {
        println!("Keyboard key down: {:#?}", key);
        if key == &Keycode::Up || key == &Keycode::W {
            let message = RedisMessage {
                motor: Motor::Both,
                direction: Direction::Forward,
                speed: 1
            };
            down_handler.load_message(message);
        } else if key == &Keycode::Down || key == &Keycode::S {
            let message = RedisMessage {
                motor: Motor::Both,
                direction: Direction::Backward,
                speed: 1
            };
            down_handler.load_message(message);
        } else if key == &Keycode::Right || key == &Keycode::D {
            let message = RedisMessage {
                motor: Motor::Left,
                direction: Direction::Forward,
                speed: 1
            };
            down_handler.load_message(message);
        } else if key == &Keycode::Left || key == &Keycode::A {
            let message = RedisMessage {
                motor: Motor::Right,
                direction: Direction::Forward,
                speed: 1
            };
            down_handler.load_message(message);
        }
    });
    let _guard = device_state.on_key_up(move |key| {
        println!("Keyboard key up: {:#?}", key);
        if key == &Keycode::Up || key == &Keycode::W {
            let message = RedisMessage {
                motor: Motor::Both,
                direction: Direction::Forward, // this is redundant
                speed: 0
            };
            up_handler.load_message(message);
        } else if key == &Keycode::Down || key == &Keycode::S {
            let message = RedisMessage {
                motor: Motor::Both,
                direction: Direction::Backward,
                speed: 0
            };
            up_handler.load_message(message);
        } else if key == &Keycode::Right || key == &Keycode::D {
            let message = RedisMessage {
                motor: Motor::Left,
                direction: Direction::Forward,
                speed: 0
            };
            up_handler.load_message(message);
        } else if key == &Keycode::Left || key == &Keycode::A {
            let message = RedisMessage {
                motor: Motor::Right,
                direction: Direction::Forward,
                speed: 0
            };
            up_handler.load_message(message);
        }
    });

    handler.spawn_tasks();

    loop {}
}
