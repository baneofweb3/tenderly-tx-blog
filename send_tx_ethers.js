const { ethers } = require ("ethers");
require ("dotenv").config();

//This variable should hold the address to which we will be sending SEP.
const destinationAddress = "";

const main = async () => {
    //provider will be our connection to the Tenderly Web3 Gateway. We pull the URL from the .env file we created earlier.
    provider = new ethers.providers.JsonRpcProvider(process.env.TENDERLY_URL);

    //Prepare the sender - this will be based on the private key we set up in the .env file.
    const sender = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

    //The balanceBefore variable will hold the balance of the destination address before we send any SEP.
    const balanceBefore = await provider.getBalance(destinationAddress); 
    console.log(`Destination balance before sending: ${ethers.utils.formatEther(balanceBefore)} ETH`);
    console.log("Sending...\n");
    
    //Here you can change how much SEP we are sending.
    const tx = await sender.sendTransaction({to: destinationAddress, value: ethers.utils.parseEther("0.001")});
    console.log("Sent! 🎉");
    console.log(`TX hash: ${tx.hash}`);
    console.log("Waiting for receipt...");

    //This line will block the script until 1 block is mined or 150s pass. That way we can be sure the transaction is complete.
    await provider.waitForTransaction(tx.hash, 1, 150000).then(() => {});

    //Print out the link to the trnasaction overview page on the Tenderly Dashboard.
    console.log(`TX details: https://dashboard.tenderly.co/tx/sepolia/${tx.hash}\n`);

    //The balanceAfter variable is retrieved the same as earlier - it will contain the new balance of the destination address.
    const balanceAfter = await provider.getBalance(destinationAddress);
    console.log(`Destination balance after sending: ${ethers.utils.formatEther(balanceAfter)} ETH`);
}

//This calls the main function, along with some standard error handling.
main ()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });