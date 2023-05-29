use std::sync::Arc;

use tokio::sync::Mutex;
use redis::{AsyncCommands, aio::Connection, Client};
use async_trait::async_trait;

use super::{PlatformHandler, Config, pack_message, RedisMessage};


#[derive(Clone)]
pub struct DesktopHandler {
    redis: Option<Arc<Mutex<Connection>>>,
    client: Client,
    rx: Arc<Mutex<tokio::sync::broadcast::Receiver<RedisMessage>>>,
    pub tx: tokio::sync::broadcast::Sender<RedisMessage>
}

#[async_trait]
impl PlatformHandler for DesktopHandler {
    fn new() -> Self {
        let config_contents = include_str!("../../../config.toml");
        let config: Config = toml::from_str(config_contents).unwrap();
        let client = redis::Client::open(config.redis.url).unwrap();
        let (tx, rx) = tokio::sync::broadcast::channel(300);

        Self {
            redis: None,
            client,
            rx: Arc::new(Mutex::new(rx)),
            tx
        }
    }

    async fn send_message(&mut self, message: super::RedisMessage) {
        println!("Sending message: {message:?}");
        if self.redis.is_none() {
            let connection = self.client.get_async_connection().await.unwrap();
            self.redis = Some(Arc::new(Mutex::new(connection)))
        }
        let conn = Arc::clone(&self.redis.clone().unwrap());
        let msg = pack_message(message);
        let mut conn_guarded = conn.lock().await;
        let _: () = conn_guarded.publish("pathfinder", msg).await.unwrap();
    }

    async fn send_task(&mut self) {
        loop {
            let message = self.rx.lock().await.recv().await.unwrap();
            self.send_message(message).await;
        }
    }

    fn load_message(&self, message: super::RedisMessage) {
        self.tx.send(message).unwrap();
    }

    fn spawn_tasks(self) {
        let mut _self = Arc::new(Mutex::new(self));
        tokio::spawn(async move {
            _self.lock().await.send_task().await;
        });
    }
}