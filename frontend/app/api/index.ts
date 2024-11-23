
export const defaultQueryFn = async (url: string, method: string) => {
    const response = await fetch(`http://127.0.0.1:8000/${ url }`, { method });
    console.log("response:",response);
    const body = await response.json();

    if (!response.ok) {
        throw new Error(`${ response.status } - ${ response.body }`);
    } else if (body.message && body.timestamp) {
        throw new Error(`403 - ${ body.message }`);
    }

    return body;
};

// POST REQUEST TO UPLOAD DATASET
export const uploadDataset =