import type React from "react";
import { useEffect, useState } from "react";
import { AiSummarizer } from "./components/ai-summarizer";
import { Button } from "./components/ui/button";
import { Textarea } from "./components/ui/textarea";
import { useToast } from "./components/ui/use-toast";
import { summarizeWebPage } from "./summarizer";
import { LanguageSelector } from "./components/LanguageSelector";
import {
	type TranscriptionLanguage,
	transcriptionSettingsAtom,
} from "./jotai/settingAtom";
import { useAtom } from "jotai";
import {
	modelLoadingProgressAtom,
	modelStatusAtom,
} from "./jotai/modelStatusAtom";

const fetchAiCapabilities = async () => {
	if (!window.ai) {
		return {
			available: "no",
		};
	}

	const { available } = await window.ai.languageModel.capabilities();

	return {
		available,
	};
};

const SidePanelApp: React.FC = () => {
	const [summary, setSummary] = useState("");
	const [transcriptionSettings, setTranscriptionSettings] = useAtom(
		transcriptionSettingsAtom,
	);
	const [isSummaryLoading, setIsSummaryLoading] = useState(false);
	const [aiCapabilities, setAiCapabilities] = useState<{ available: string }>({
		available: "no",
	});
	const [transcription, setTranscription] = useState("");
	const [modelStatus, setModelStatus] = useAtom(modelStatusAtom);
	const [loadingProgress, setLoadingProgress] = useAtom(
		modelLoadingProgressAtom,
	);

	useEffect(() => {
		fetchAiCapabilities().then((capabilities) => {
			setAiCapabilities(capabilities);
		});

		chrome.runtime.onMessage.addListener((message) => {
			if (message.type === "transcript") {
				console.debug("Received transcript message", message.data.transcripted);
				setTranscription((prev) => `${prev}\n${message.data.transcripted}`);
			} else if (message.type === "model-status") {
				console.debug("Received model status", message.data.status);
				setModelStatus(message.data.status);
				if (message.data.status === "loading") {
					setLoadingProgress(message.data.progress);
				}
			}
		});
	}, [setModelStatus, setLoadingProgress]);

	const { toast } = useToast();

	const handleSummarize = async () => {
		setIsSummaryLoading(true);
		try {
			const result = await summarizeWebPage(transcriptionSettings.language);
			setSummary(result);
			toast({
				description: "Summarized",
				color: "success",
			});
		} catch (error) {
			console.error(error);
			setSummary(`Failed to summarize: ${error}`);
			toast({
				description: "Failed to summarize",
				color: "error",
			});
		} finally {
			setIsSummaryLoading(false);
		}
	};

	const language: TranscriptionLanguage =
		transcriptionSettings.language as TranscriptionLanguage;

	return (
		<div className="container">
			<div className="box-border">
				{/* Transcription from web speech api */}
				<div className="flex flex-col m-1 p-1">
					<h1>Transcription</h1>
					<div className="text-center mt-1">
						<Textarea value={transcription} rows={20} readOnly />
					</div>
					{/* model status */}
					<div className="text-center">
						<h1>Model Status: {modelStatus}</h1>
						{modelStatus === "loading" && <p>{loadingProgress}% loaded</p>}
					</div>
				</div>
				<div className="flex flex-col m-1 p-1">
					<LanguageSelector
						language={language}
						setLanguage={(language: TranscriptionLanguage) =>
							setTranscriptionSettings((prev) => {
								return { ...prev, language };
							})
						}
					/>
				</div>
				{/* record button */}
				{/* <div className="flex flex-col m-1 p-1">
          <Button
            onClick={() => chrome.runtime.sendMessage({ type: "startCapture" })}
          >
            Stop Recording
          </Button>
        </div> */}
				{/* if status is unknown or error, show loading model button */}
				{/* {(modelStatus === "unknown" || modelStatus === "error") && (
          <div className="flex flex-col m-1 p-1">
            <Button
              onClick={() =>
                chrome.runtime.sendMessage({
                  type: "initialize-transcription-model",
                })
              }
            >
              Load Model
            </Button>
          </div>
        )} */}

				{/* copy to clipboard button */}
				<div className="flex flex-col m-1 p-1">
					<Button
						onClick={() => {
							navigator.clipboard.writeText(transcription);
							toast({
								description: "Copied to clipboard",
								color: "success",
								duration: 1000,
							});
						}}
					>
						Copy to Clipboard
					</Button>
				</div>

				{aiCapabilities.available === "no" && (
					<div className="flex flex-col m-1 p-1">
						<div className="text-center">
							<h1>AI Summarization is not available</h1>
							<p>
								AI Summarization is not available. Please make sure your chrome
								supports Prompt API.
							</p>
						</div>
					</div>
				)}
				{aiCapabilities.available !== "no" && (
					<AiSummarizer
						setLanguage={(language: TranscriptionLanguage) =>
							setTranscriptionSettings((prev) => {
								return { ...prev, language: language };
							})
						}
						language={transcriptionSettings.language}
						isSummaryLoading={isSummaryLoading}
						handleSummarize={handleSummarize}
						summary={summary}
					/>
				)}
			</div>
		</div>
	);
};

export default SidePanelApp;
