// src/components/PromptArea.tsx
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { SendIcon } from "lucide-react";

interface PromptAreaProps {
  onSendPrompt: (prompt: string) => void;
}

export const PromptArea: React.FC<PromptAreaProps> = ({ onSendPrompt }) => {
  const [prompt, setPrompt] = useState("");

  const handleSendPrompt = () => {
    if (prompt.trim() !== "") {
      onSendPrompt(prompt);
      setPrompt("");
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <Textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows={4}
        placeholder="Enter your prompt here..."
      />
      <Button onClick={handleSendPrompt}>
        <SendIcon className="mr-2 h-4 w-4" /> Send
      </Button>
    </div>
  );
};