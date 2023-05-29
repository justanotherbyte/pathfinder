mod desktop;

use serde::{Serialize, Deserialize};
use async_trait::async_trait;

pub use desktop::DesktopHandler as MessageHandler;

#[async_trait]
pub trait PlatformHandler {
    fn new() -> Self;

    fn load_message(&self, message: RedisMessage);
    fn spawn_tasks(self);
    async fn send_message(&mut self, message: RedisMessage);
    async fn send_task(&mut self);
}

#[derive(Serialize, Deserialize, Clone, Copy, Debug)]
pub enum Motor {
    Left,
    Right,
    Both,
    Pivot(bool)
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct RedisMessage {
    pub motor: Motor,
    pub speed: u16
}

#[derive(Deserialize)]
pub struct RedisConfig {
    pub url: String
}

#[derive(Deserialize)]
pub struct Config {
    pub redis: RedisConfig
}

pub fn pack_message(message: RedisMessage) -> Vec<u8> {
    let json_string = serde_json::to_string(&message).unwrap();
    let mut buf = Vec::new();
    rmp::encode::write_str(&mut buf, &json_string).unwrap();
    buf
}