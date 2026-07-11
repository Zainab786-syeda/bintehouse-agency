document.addEventListener('DOMContentLoaded', () => {
    const toolsContainer = document.getElementById("tools-container");
    const searchInput = document.querySelector('.search-box');
    let allTools = []; // Database se aane wale saare tools is array mein save honge

    // 1. Flask API se Supabase Cloud ka data load karne ka fetch call
    fetch("/api/ai-tools")
        .then(response => response.json())
        .then(tools => {
            allTools = tools; // Global array ko populate kiya taake search query is par run ho sake
            displayTools(allTools); // Tools ko interface par render karne ka main function call kiya
        })
        .catch(error => {
            console.error("Error fetching AI tools:", error);
            if (toolsContainer) {
                toolsContainer.innerHTML = "<p style='color: #ef4444;'>Error loading AI tools. Please refresh the page.</p>";
            }
        });

    // 2. Tools ko HTML grid card markup ke mutabiq load karne ka function
    function displayTools(toolsList) {
        if (!toolsContainer) return;
        
        if (toolsList.length === 0) {
            toolsContainer.innerHTML = "<p style='color: #9ca3af; font-style: italic;'>No matching AI tools found.</p>";
            return;
        }

        toolsContainer.innerHTML = ""; // Pehle se maujood template text saaf karein

        // Har tool ka loop chala kar use aap ke original template design mein convert kiya
        toolsList.forEach(tool => {
            toolsContainer.innerHTML += `
                <div class="tool-card">
                    <h3>${tool.tool_name}</h3>
                    <p>${tool.description || 'Explore this amazing AI tool on our hub.'}</p>
                    <div class="tool-footer">
                        <span class="tag">${tool.category || 'AI Tool'}</span>
                        <a href="${tool.tool_link}" target="_blank" class="visit-btn">Use Tool</a>
                    </div>
                </div>
            `;
        });
    }

    // 3. Live Dynamic Search Engine Feature
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase().trim();

            // Cloud data content ko filter logic lagakar scan karna
            const filteredTools = allTools.filter(tool => {
                const toolName = (tool.tool_name || "").toLowerCase();
                const toolDesc = (tool.description || "").toLowerCase();
                const toolCat  = (tool.category || "").toLowerCase();

                return toolName.includes(searchTerm) || 
                       toolDesc.includes(searchTerm) || 
                       toolCat.includes(searchTerm);
            });

            // Filtered array list ko grid layout par dubara refresh karna
            displayTools(filteredTools);
        });
    }
});
