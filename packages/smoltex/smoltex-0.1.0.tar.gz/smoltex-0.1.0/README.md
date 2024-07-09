# smoltex

Convert natural language descriptions to LaTeX equations within your terminal in under one second!

![usage](./media/smoltex.png)


## how to use?

> This project uses [Groq](https://groq.com) platform for very fast response generation, so you will need to setup an API key for it. Groq provides a free tier API for personal usage.

To use **smoltex** you need to follow two simple steps:

**Step 1: setup**

- Visit the [Groq console](https://console.groq.com/docs/quickstart) to create your API key for free.

- Then in the terminal of your choice, paste the below line:

```shell
export GROQ_API_KEY=<your-api-key-here>
```

or add this line to your `.bashrc` or `.zshrc` file for persistent usage.


**Step 2: use**

In the current terminal session, the command for using smoltex is `smoltex` followed by the natural language description of the latex equation you want:

```shell
smoltex "equation for cross entropy"
```

The output will be the latex string of the requested description. You can paste the equation in any latex renderer to see the result.

That's it.


## available models

Using the `-m` or `--model_name` option, you can choose to generate the latex string with different models as well. Available models (as of now) are:

```
Llama 3 variants:
- llama3-8b-8192
- llama3-70b-8192

Gemma variants:
- gemma-7b-it
- gemma2-9b-it

Mistral variants:
- mixtral-8x7b-32768
```

**Example command for different models**:

```shell
smoltex "equation for cross entropy" -m "mixtral-8x7b-32768"
```