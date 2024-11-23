
export const defaultQueryFn = async (url: string, method: string) => {
    const response = await fetch(`http://127.0.0.1:8000/${ url }`, { method });
    const body = await response.json();

    if (!response.ok) {
        throw new Error(`${ response.status } - ${ response.body }`);
    } else if (body.message && body.timestamp) {
        throw new Error(`403 - ${ body.message }`);
    }

    return body;
};


// export default async function handler(req: NextApiRequest, res: NextApiResponse) {

//     if (req.method !== "GET") {
//         res.status(405).send({ message: "Forbidden" });
//         return;
//     }

//     const { userGUID, careerGUID } = req.query;

//     const init: RequestInit = {
//         method: req.method,
//         headers: {
//             "Authorization": `Bearer ${ token }`,
//         },
//     };

//     try {
//         const response = await fetch(`http://127.0.0.1:8000/${url}`, init);
//         const data = await response.json();

//             if (!response.ok) {
//                 // get error message from body or default to response status
//                 const error = (data && data.message) || response.status;
//                 return res.status(response.status).json({ error: error });
//             }

//             return res.status(200).json({ isInMyList: isInMyList });
//         }

//     } catch (err) {
//         res.status(500).json({ error: 'Unable to check if career is in list' });
//     }
// }
