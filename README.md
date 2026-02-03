# Ai_Applications
ai/llm applications (ollama)


Based on this description: https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image
```
On the Mac
Ollama handles running the model with GPU acceleration. It provides both a simple CLI as well as a REST API for interacting with your applications.

To get started, simply download and install Ollama.

On the Mac, please run Ollama as a standalone application outside of Docker containers as Docker Desktop does not support GPUs.
```


cleanup:
```
Manual deletion: HuggingFace models are stored in the .cache folder. On a Mac, you can find it at /Users/USER_NAME/.cache/torch/transformers/. You can manually delete larger files and then re-run textEmbed() to download necessary models again ².

List installed models: Run ollama list to see the models installed on your system.
Delete a model: Use ollama rm <model name> to delete a specific model. For example, ollama rm llama3.2:latest.
Confirm deletion: Run ollama list again to verify the model has been deleted.
Locate model files: Ollama models are stored in C:\Users\<user name>\.ollama on Windows. You can manually delete files from this directory ¹.
```

delete ollama
```
sudo rm -rf /Applications/Ollama.app
sudo rm /usr/local/bin/ollama
rm -rf "~/Library/Application Support/Ollama"
rm -rf "~/Library/Saved Application State/com.electron.ollama.savedState"
rm -rf ~/Library/Caches/com.electron.ollama/
rm -rf ~/Library/Caches/ollama
rm -rf ~/Library/WebKit/com.electron.ollama
rm -rf ~/.ollama
```