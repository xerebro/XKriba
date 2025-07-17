// src/utils/generateResponse.ts
import { AutoTokenizer, AutoModelForCausalLM } from "@huggingface/transformers";

export async function generateResponse(prompt: string, transcript: string): Promise<string> {
  const tokenizer = await AutoTokenizer.from_pretrained("Xenova/Qwen1.5-0.5B-Chat");
  const model = await AutoModelForCausalLM.from_pretrained("Xenova/Qwen1.5-0.5B-Chat");

  const inputText = `${prompt}\n${transcript}`;
  const inputs = tokenizer.encode(inputText, { return_tensors: "pt" });

  const output = await model.generate(inputs, { max_length: 500 });
  const response = tokenizer.decode(output[0], { skip_special_tokens: true });

  return response;
}