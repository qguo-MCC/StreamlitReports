from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import FAISS
from timeit import timeit
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
large_orca_path = (
    r"C:/Users/qguo/PycharmProjects/GPT4AllModels/orca-mini-13b.ggmlv3.q4_0.bin"  # replace with your desired local file path
)
small_orca_path = (
    r"C:/Users/qguo/PycharmProjects/GPT4AllModels/orca-mini-3b.ggmlv3.q4_0.bin"  # replace with your desired local file path
)

# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]

# Verbose is required to pass to the callback manager
llm_large = GPT4All(model=large_orca_path, callbacks=callbacks, verbose=True)
llm_small = GPT4All(model=small_orca_path, callbacks=callbacks, verbose=True)



llm_chain_large = LLMChain(prompt=prompt, llm=llm_large)
llm_chain_small = LLMChain(prompt=prompt, llm=llm_small)
question = "summarize the following paragraph in one sentence: The Hall of the Saints or the Sala dei Santi is a room in the Borgia Apartment of the Vatican Palace, frescoed by the Italian Renaissance artist, Pinturicchio. It dates to 1491–1494 and was commissioned by Pope Alexander VI. The frescoes depict scenes from the lives of the saints. The ceiling fresco, which depicts myths related to the ancient Egyptian gods Osiris and Isis, has been the subject of much scholarly attention.[1] The iconographic program reflects the humanistic interests of Alexander and was likely designed by his secretary, Giovanni Annio of Viterbo.[2]"

timeit(lambda: llm_chain_large.run(question))
timeit(lambda: llm_chain_small.run(question))

#embedding
embedding_path = "C:/Users/qguo/PycharmProjects/GPT4AllModels/ggml-all-MiniLM-L6-v2-f16.bin"
gpt4all_embd = GPT4AllEmbeddings(model = embedding_path)
text = "This is a test document."
query_result = gpt4all_embd.embed_query(text)
doc_result = gpt4all_embd.embed_documents([text])

#db = FAISS.from_documents(docs, gpt4all_embd)